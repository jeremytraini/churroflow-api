# SENG2021 23T1 CHURROS E-Invoicing Validation API

In order to run the server, we must
- be running a Postgres database server with a database named "validation"
- be inside a python3 virtual environment
- install the necessary modules inside this virtual environment
- set the appropriate envrionment variables for the database
- run the server

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

### Setting environment variables for database
So that the server knows what database to connect to, run
```bash
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5433
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_DB=validation
```
Note: ensure these match the settings on the Postgres server you are running. The port may be 5432 and the password is whatever you set it to be when setting up the database.

### Run the server
Finally, to run the server, simply execute in the main repo folder:
```bash
python3 -m src.main
```

### Run tests
To run the tests, first run the server, then run
```bash
pytest
```

## Deployment Link
http://churros.eba-pyyazat7.ap-southeast-2.elasticbeanstalk.com/docs
