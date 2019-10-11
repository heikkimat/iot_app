from flask import Flask, request, jsonify, render_template, abort
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os
import config
from datetime import datetime
import pytz
from pytz import timezone

# Init app
app = Flask(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
# Database
ENV = 'prod'

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
  hum = db.Column(db.Float)

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

# Show recent db entry
@app.route("/")
def index():
    temphum = TempHum.query.order_by(TempHum.id.desc()).first_or_404()
    #return th_schema.jsonify(temphum)

    #t_pst1 = t.astimezone(pytz.timezone('Europe/Helsinki'))
    #time_stamp1 = t_pst1.strftime('%I:%M:%S %p   %b %d, %Y')

    return render_template("showtemphum.html", data1=temphum.temp, data2=temphum.hum, 
                            timestamp=temphum.timestamp.astimezone(pytz.timezone('Europe/Helsinki')).strftime('%H:%M:%S   %d.%m.%Y'))

# Create a row in db
@app.route('/update', methods=['POST'])
def update():
  api_key = request.form['api_key']
  mac = request.form['mac']
  temp = request.form['temp']
  hum = request.form['hum']
  # check if the api key and mac address are correct
  if (api_key == 'API_KEY' and mac == 'MAC_ADDRESS'):
    try:
      t = datetime.now(timezone('Europe/Helsinki'))
      #date_time_str = t.isoformat()
      new_temp_hum = TempHum(t, temp, hum)

      db.session.add(new_temp_hum)
      db.session.commit()

      return th_schema.jsonify(new_temp_hum)
    except: #when temp or hum is not numeric
      abort(400, 'Check the parameters')
  else:
      abort(401, description="Your are not authorized to update db")

#testing REST
@app.route("/show/API_key=<api_key>/mac=<mac>/temp=<temp>/hum=<hum>", methods=['GET'])
def write_data_point(api_key, mac, temp, hum):
    if (api_key == 'API_KEY' and mac == 'MAC_ADDRESS'):
        t = datetime.now(timezone('Europe/Helsinki'))
        #date_time_str = t.isoformat()

        return render_template("showtemphum.html", data1=temp, data2=hum, timestamp=t.strftime('%I:%M:%S %p   %b %d, %Y'))


    else:
        return "403"

# Run Server
if __name__ == '__main__':
  app.run()