# REST API With Flask & SQL Alchemy

> Products API using Python Flask, SQL Alchemy and Marshmallow

## Quick Start Using Pipenv

``` bash
# Activate venv
$ pipenv shell

# Install dependencies
$ pipenv install

# Create DB
$ python
>> from app import db
>> db.create_all()
>> exit()

# Run Server (http://localhst:5000)
python app.py
```

## Endpoints

* GET     /update/API_key=<api_key>/mac=<mac>/temp=<temp>/hum=<hum>
* POST     /update/API_key=<api_key>/mac=<mac>/temp=<temp>/hum=<hum>

