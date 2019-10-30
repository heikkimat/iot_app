from flask import Flask, request, jsonify, render_template, abort, url_for, make_response
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os
import config
from datetime import datetime, timedelta
import pytz
from pytz import timezone
from flask_cors import CORS, cross_origin

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

CORS(app)

# Current time
def time_now():
  return datetime.now(timezone('Europe/Helsinki'))

# IOT data update Class/Model
class TempHum(db.Model):
  __tablename__ = 'temp2_hum'
  id = db.Column(db.Integer, primary_key=True)
  timestamp = db.Column(db.DateTime(timezone=True))
  #description = db.Column(db.String(200))
  temp = db.Column(db.Float)
  temp2 = db.Column(db.Float)
  hum = db.Column(db.Float)

  def __init__(self, timestamp, temp, temp2, hum):
    self.timestamp = timestamp
    self.temp = temp
    self.temp2 = temp2
    self.hum = hum

# Product Schema
class ThSchema(ma.Schema):
  class Meta:
    fields = ('id', 'timestamp', 'temp', 'temp2', 'hum')

# Init schema
th_schema = ThSchema()
th_schemas = ThSchema(many=True)

# Show recent db entry
@app.route("/")
def index():
  temphum = TempHum.query.order_by(TempHum.id.desc()).all()
  return render_template("showtemphum.html", temphum=temphum)
  #t_pst1 = t.astimezone(pytz.timezone('Europe/Helsinki'))
  #time_stamp1 = t_pst1.strftime('%I:%M:%S %p   %b %d, %Y')
  #return render_template("showtemphum.html", data1=temphum.temp, data2=temphum.hum, data3=temphum.temp2, timestamp=temphum.timestamp.astimezone(pytz.timezone('Europe/Helsinki')).strftime('%d.%m.%Y  -  %H:%M:%S'))

# Create a row in db
@app.route('/update', methods=['POST'])
def update():
  api_key = request.form['api_key']
  mac = request.form['mac']
  temp = request.form['temp']
  temp2 = request.form['temp2']
  hum = request.form['hum']
  # check if the api key and mac address are correct
  if (api_key == 'API_KEY' and mac == 'MAC_ADDRESS'):
    try:
      t = datetime.now(timezone('Europe/Helsinki'))
      #date_time_str = t.isoformat()
      new_temp_hum = TempHum(t, temp, temp2, hum)

      db.session.add(new_temp_hum)
      db.session.commit()

      return th_schema.jsonify(new_temp_hum)
    except: #when temp or hum is not numeric
      abort(400, 'Check the parameters')
  else:
      abort(401, description="Your are not authorized to update db")

#data fetched by app.js
@app.route("/data", methods=['GET','POST'])
def data():
  req = request.get_json()
  print(req['range'])
  today = datetime.now(timezone('Europe/Helsinki'))
  today = today.replace(hour=0, minute=0, second=0, microsecond=0)
  temp_hum = TempHum.query.filter(TempHum.timestamp >= today).order_by(TempHum.id.asc()).all()
  return th_schemas.jsonify(temp_hum)
""" 
#testing REST
@app.route("/show/API_key=<api_key>/mac=<mac>/temp=<temp>/hum=<hum>", methods=['GET'])
def write_data_point(api_key, mac, temp, hum):
    if (api_key == 'API_KEY' and mac == 'MAC_ADDRESS'):
        t = datetime.now(timezone('Europe/Helsinki'))
        #date_time_str = t.isoformat()

        return render_template("showtemphum.html", data1=temp, data2=hum, timestamp=t.strftime('%I:%M:%S %p   %b %d, %Y'))


    else:
        return "403"

 """
 # Run Server
if __name__ == '__main__':
  app.run()