## An example

![image](https://github.com/user-attachments/assets/dba0ea54-c644-4234-a5e4-26fc18fd50d7)

## How to run the application

### Creation of virtual environments is done by executing the command venv:

`python -m venv .venv`

### Install requirements

`pip install -r requirements.txt`

### Create .env files with these keys

https://fireworks.ai/account/api-keys

> DB_CONNECTION_STRING="mssql+pyodbc://<username>:<password>@<server-name>/<db-name>?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"
> FIREWORKS_API_KEY='xxx'

### Run the app

`streamlit run app.py`

## [Demo](https://minh-sql-agent.streamlit.app/)

## TODO

- Message history
- Dynamic LLMs with dynamic model names
