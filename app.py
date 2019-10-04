from flask import Flask, request, jsonify, render_template, abort
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os
import config
from datetime import datetime
from pytz import timezone

# Init app
app = Flask(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
# Database
ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = config.local_postgres
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = config.hero_postgres

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Current time
def time_now():
  return datetime.now(timezone('Europe/Helsinki'))

# Product Class/Model
class TempHum(db.Model):
  __tablename__ = 'temp_hum'
  id = db.Column(db.Integer, primary_key=True)
  timestamp = db.Column(db.DateTime(timezone=True))
  #description = db.Column(db.String(200))
  temp = db.Column(db.Float)
  hum = db.Column(db.Integer)

  def __init__(self, timestamp, temp, hum):
    self.timestamp = timestamp
    self.temp = temp
    self.hum = hum

# Product Schema
class ThSchema(ma.Schema):
  class Meta:
    fields = ('id', 'timestamp', 'temp', 'hum')

# Init schema
th_schema = ThSchema()
#products_schema = ProductSchema(many=True)

# Create a row in db
@app.route('/update/API_key=<api_key>/mac=<mac>/temp=<temp>/hum=<hum>', methods=['GET','POST'])
def update(api_key, mac, temp, hum):
  
  if (api_key == 'API_KEY' and mac == 'MAC_ADDRESS'):
      t = datetime.now(timezone('Europe/Helsinki'))
      #date_time_str = t.isoformat()
      new_temp_hum = TempHum(t, temp, hum)

      #db.session.add(new_temp_hum)
      #db.session.commit()

      return th_schema.jsonify(new_temp_hum)

  else:
      abort(401, description="Your are not authorized to update db")
  
  
# Get All Products
@app.route('/product', methods=['GET'])
def get_products():
  all_products = Product.query.all()
  result = products_schema.dump(all_products)
  return jsonify(result)

# Get Single Products
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
  product = Product.query.get(id)
  return product_schema.jsonify(product)

# Update a Product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
  product = Product.query.get(id)

  name = request.json['name']
  description = request.json['description']
  price = request.json['price']
  qty = request.json['qty']

  product.name = name
  product.description = description
  product.price = price
  product.qty = qty

  db.session.commit()

  return product_schema.jsonify(product)

# Delete Product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
  product = Product.query.get(id)
  db.session.delete(product)
  db.session.commit()

  return product_schema.jsonify(product)

@app.route("/show/API_key=<api_key>/mac=<mac>/field=<int:field>/data=<data>", methods=['GET'])
def write_data_point(api_key, mac, field, data):
    if (api_key == 'API_KEY' and mac == 'MAC_ADDRESS'):
        t = datetime.now(timezone('Europe/Helsinki'))
        date_time_str = t.isoformat()

        return render_template("showrecent.html", data=data, time_stamp=date_time_str)

    else:
        return "403"

# Run Server
if __name__ == '__main__':
  app.run()