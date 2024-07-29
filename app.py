import os

import streamlit as st
from dotenv import load_dotenv
from langchain.agents.agent import AgentExecutor
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_fireworks import ChatFireworks

from sql_agent import create_sql_agent_executor

load_dotenv()

DB_CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING')
FIREWORKS_API_KEY = os.getenv('FIREWORKS_API_KEY')
DEFAULT_MAX_ITERATIONS = 6


def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "api_key" not in st.session_state:
        st.session_state.api_key = FIREWORKS_API_KEY

    if "connection_string" not in st.session_state:
        st.session_state.connection_string = DB_CONNECTION_STRING

    if "max_iterations" not in st.session_state:
        st.session_state.max_iterations = DEFAULT_MAX_ITERATIONS


def render_sidebar():
    with st.sidebar:
        st.info("If these variables are not provided\n`.env` file will be used")

        api_key = st.text_input(
            label="[Fireworks API Key](https://fireworks.ai/account/api-keys): ",
            placeholder='48 chars api key'
        )

        connection_string = st.text_area(
            label="DB Connection String: ",
            placeholder="mssql+pyodbc://<username>:<password>@<server-name>/<db-name>?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"
        )

        max_iterations = st.text_input(
            label="Max Iterations: ",
            placeholder='6'
        )

        st.session_state.api_key = api_key or os.getenv('FIREWORKS_API_KEY')
        st.session_state.connection_string = connection_string or os.getenv(
            'DB_CONNECTION_STRING')
        st.session_state.max_iterations = max_iterations or DEFAULT_MAX_ITERATIONS


def render_notices():
    with st.expander("Notices", expanded=False):
        st.write(
            """
            - Make sure input key in the `sidebar` on the left **OR** input key in `.env` before asking questions
            - If you see the _"Agent stopped due to iteration limit or time limit"_ message. You can increase the `max_iterations` parameter to limit the maximum number of steps to take before ending the execution loop.
            - Other LLMs (https://python.langchain.com/v0.2/docs/integrations/chat/)
            """
        )


def render_chat(agent_executor: AgentExecutor):
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Ask me any questions"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.spinner("Loading..."):
            with st.chat_message("assistant"):
                # Display thoughts and actions
                # for testing purposes only
                st_callback = StreamlitCallbackHandler(st.container())

                response = agent_executor.invoke(prompt, {
                    "callbacks": [st_callback]
                })

                output = response.get('output')

                st.markdown(output)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": output
            }
        )


def main():

    st.set_page_config(page_title="SQL Agent")

    st.title("SQL Agent")

    init_session_state()
    render_sidebar()
    render_notices()

    if not st.session_state.api_key or not st.session_state.connection_string:
        st.error("API Key or DB Connection String is not provided")
    else:

        llm = ChatFireworks(
            model="accounts/fireworks/models/llama-v3-70b-instruct",
            api_key=st.session_state.api_key,
            temperature=0
        )

        agent_executor = create_sql_agent_executor(
            llm=llm,
            connection_string=st.session_state.connection_string,
            max_iterations=st.session_state.max_iterations
        )

        render_chat(agent_executor)


if __name__ == "__main__":
    main()
