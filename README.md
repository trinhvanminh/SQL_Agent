## What is this?
It’s similar to AI **text2SQL** bots, but with added information:
- Table names in your SQL database
- Schema details for each table
- Sample rows from each table
This makes it more accurate and includes the query results as well.

**FYI**: In the example below, you can see the previous steps. Clicking on them will show you the process it followed to generate the SQL query, including the final query that provides the answer.

## An example

![image](https://github.com/user-attachments/assets/dba0ea54-c644-4234-a5e4-26fc18fd50d7)

## How to run the application

### Creation of virtual environments is done by executing the command venv:

`python -m venv .venv`

### Active venv (window)

`.\.venv\Scripts\activate`

### Install requirements

`pip install -r requirements.txt`

### Create .env files with these keys

> DB_CONNECTION_STRING="mssql+pyodbc://<username>:<password>@<server-name>/<db-name>?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"
> FIREWORKS_API_KEY='xxx'

You can get the `FIREWORKS_API_KEY` [here](https://fireworks.ai/account/api-keys). 

There are a lot of LLM services to choose such as *AzureOpenAI, OpenAI, Cohere, Ollama, Groq, Fireworks, GoogleGenerativeAI,...*
Feel free to make pull requests or make a request to me if you interested
### Run the app

`streamlit run app.py`

## [Demo](https://minh-sql-agent.streamlit.app/)

## TODO

- Message history
- Dynamic LLMs with dynamic model names
