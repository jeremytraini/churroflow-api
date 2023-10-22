# ChurroFlow API

Welcome to ChurroFlow API, an invoice validation and processing solution. This API underpins the ChurroFlow web application, which you can find [here](http://www.churroflow.com).

## The Team
- **Jeremy Traini** - Team Lead
- **Ricardo Alkazzi** - Product Owner
- **Ahona Dutta** - Scrum Master
- **Denzel Iskandar** - Delivery Manager


## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Deployment](#deployment)
- [Installation](#installation)
- [Usage](#usage)
- [Routes & Endpoints](#routes--endpoints)

## Introduction

Many business owners face challenges adopting the PEPPOL invoicing system due to the technical knowledge and resources required. Our interactive invoice validator simplifies this integration, offering a user-friendly platform to edit and validate invoices.

## Features

- **Real-time Validation:** Instant feedback on the wellformedness, syntax, schema, and PEPPOL standards of your invoices.
- **Bulk Operations:** Upload, validate, and export multiple invoices simultaneously.
- **Detailed Reports:** Access a comprehensive report detailing errors, suggestions, and more.
- **Secure User Authentication:** Register, login, and manage your sessions with JWT authentication.
- **Interactive Dashboards:** A visually appealing dashboard to overview your business's invoice statistics.
- **Warehouse Analytics:** Dive deep into your warehouse operations with data-rich graphs and heatmaps.

## Deployment

The ChurroFlow API is currently deployed on AWS Elastic Beanstalk and is hosted at [api.churroflow.com](http://api.churroflow.com). You can interact directly with the API through this endpoint.

## Installation

If you want to run it locally, you can:

First ensure that you have a postgresql database running on your machine with a database named `validation`. To set up the database, run the following commands:

```bash
sudo service postgresql start
sudo -u postgres psql
CREATE DATABASE validation;
\q

export POSTGRES_HOST=localhost
export POSTGRES_PORT=5433
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_DB=validation
```

Then, clone the repository and run the following commands:
```bash
git clone https://github.com/jeremytraini/churroflow-api.git
cd churroflow-api
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt

python3 -m src.main
```

Make sure you have Python and the necessary dependencies installed.

## Routes & Endpoints

You can find a comprehensive list of routes and their descriptions in the [ENDPOINTS.md](ENDPOINTS.md) file.

## Testing

To run the suite of tests, run the following command:

```bash
python3 -m pytest
```
