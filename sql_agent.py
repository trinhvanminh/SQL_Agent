import os
from typing import List


from langchain.agents.agent import AgentExecutor
from langchain.agents.types import AgentType
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.tools import BaseTool
from langchain_community.tools.sql_database.tool import (InfoSQLDatabaseTool,
                                                         ListSQLDatabaseTool,
                                                         QuerySQLCheckerTool,
                                                         QuerySQLDataBaseTool)
from langchain_community.utilities import SQLDatabase


CUSTOM_QUERY_CHECKER = """
    {query}
    Double check the {dialect} query above for common mistakes, including:
    - Using NOT IN with NULL values
    - Using UNION when UNION ALL should have been used
    - Using BETWEEN for exclusive ranges
    - Data type mismatch in predicates
    - Properly quoting identifiers
    - Using the correct number of arguments for functions
    - Casting to the correct data type
    - Using the proper columns for joins

    IMPORTANT: make sure the query is match with the {dialect}.

    If there are any of the above mistakes, rewrite the query. If there are no mistakes, just reproduce the original query.

    Output the final SQL query only.

    SQL Query: """


class CustomSQLDatabaseToolkit(SQLDatabaseToolkit):
    """Custom Toolkit for interacting with SQL databases"""

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        list_sql_database_tool = ListSQLDatabaseTool(db=self.db)
        info_sql_database_tool_description = (
            "Input to this tool is a comma-separated list of tables, output is the "
            "schema and sample rows for those tables. "
            "Be sure that the tables actually exist by calling "
            f"{list_sql_database_tool.name} first! "
            "Example Input: table1, table2, table3"
        )
        info_sql_database_tool = InfoSQLDatabaseTool(
            db=self.db, description=info_sql_database_tool_description
        )
        query_sql_database_tool_description = (
            "Input to this tool is a detailed and correct SQL query, output is a "
            "result from the database. If the query is not correct, an error message "
            "will be returned. If an error is returned, rewrite the query, check the "
            "query, and try again. If you encounter an issue with Unknown column "
            f"'xxxx' in 'field list', use {info_sql_database_tool.name} "
            "to query the correct table fields."
        )
        query_sql_database_tool = QuerySQLDataBaseTool(
            db=self.db, description=query_sql_database_tool_description
        )
        query_sql_checker_tool_description = (
            "Use this tool to double check if your query is correct before executing "
            "it. Always use this tool before executing a query with "
            f"{query_sql_database_tool.name}!"
        )

        # CUSTOMIZATION
        query_sql_checker_tool = QuerySQLCheckerTool(
            db=self.db, llm=self.llm, description=query_sql_checker_tool_description, template=CUSTOM_QUERY_CHECKER)

        return [
            query_sql_database_tool,
            info_sql_database_tool,
            list_sql_database_tool,
            query_sql_checker_tool,
        ]


def create_sql_agent_executor(llm, connection_string: str,  max_iterations: int = 6, **kwargs) -> AgentExecutor:
    # Step 1: Define connection and SQL DB
    db = SQLDatabase.from_uri(connection_string)

    # Step 2: Define SQL Database tools
    toolkit = CustomSQLDatabaseToolkit(db=db, llm=llm)

    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        agent_executor_kwargs={
            "handle_parsing_errors": True,
            # "return_intermediate_steps": True,
        },
        max_iterations=max_iterations,
        **kwargs,
    )

    return agent_executor
