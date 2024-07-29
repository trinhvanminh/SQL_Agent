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

## TODO

- Message history
- Dynamic LLMs with dynamic model names
