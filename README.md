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

* POST     /update
   * Content-Type: application/x-www-form-urlencoded
   * Body: api_key=API_KEY&mac=MAC_ADDRESS&temp=20.5&hum=55.2&temp2=21.1
* POST     /data
   * headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json;charset=UTF-8'
    },
   * body: JSON.stringify({range: selectedValue})
* GET     /clean
* GET     /

