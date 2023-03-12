# se2021-23t1-einvoicing-api-template


In order to run the server, we must
- be running a Postgres database server with a database named "validation"
- be inside a python3 virtual environment
- install the necessary modules inside this virtual environment

## Instructions below

### Setup database
To download and setup the database within WSL, follow [this tutorial](https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-database).

Run the Postgres server with
```bash
sudo service postgresql start
```

When first setting up, we must create a database named "validation"
First, run
```bash
sudo -u postgres psql
```
Then press enter after typing
```sql
CREATE DATABASE validation;
```

### Setup virtual environment
To setup the virtual environment, navigate to the repo folder and run 
```bash
python3 -m venv env
```

### Install the required modules
To install the required modules in the previously setup virtual environment, run: 
```bash
source env/bin/activate && pip3 install -r requirements.txt
```
This will start the virtual environment then pip install the needed modules

### Run the server
Finally, to run the server, simply execute in the main repo folder:
```bash
python3 -m src.server
```

### Run tests
To run the tests, first run the server, then run
```bash
pytest
```
