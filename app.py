from flask import Flask, json, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
# dialect+driver://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/test'
db = SQLAlchemy(app)
CORS(app)

@app.route('/')
def index():
  return 'index'

class CarInformation(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  year = db.Column(db.Numeric(4))
  brand = db.Column(db.String(50))
  model = db.Column(db.String(50))
  cost = db.Column(db.String(50))
  cleanTitle = db.Column(db.Boolean, default=False)
  notes = db.Column(db.String(120))

  def __init__(self, year, brand, model, cost, cleanTitle, notes):
    self.year = year
    self.brand = brand
    self.model = model
    self.cost = cost
    self.cleanTitle = cleanTitle
    self.notes = notes

@app.route('/upload', methods=['POST', 'GET'])
def upload():
  year = request.form['year']
  brand = request.form['brand']
  model = request.form['model']
  cost = request.form['cost']
  cleanTitle = request.form['cleanTitle']
  notes = request.form['notes']
  # images = request.files['file']

  # if cleanTitle == 'true':
  #   cleanTitle = True
  # elif cleanTitle == 'false': 
  #   cleanTitle = False
  # images.save('./cars/{}'.format())
  print(year)
  print(brand)
  print(model)
  print(cost)
  print(cleanTitle)
  print(notes)
  # print(request.files)
  # print('images-->', 'images')
  # print(images)
  for img in request.files:
    print(request.files[img].filename)
  # print('./cars/{}'.format(img.filename))
  # print(request.files)

  # CarInfo = CarInformation(year, brand, model, cost, cleanTitle, notes)
  # db.session.add(CarInfo)
  # db.session.commit()

  return 'Success'
  # return json.dumps({'brand': 'brand'})

# @app.route('/upload', methods=['POST', 'GET'])
# def upload():
#     year = request.form['year']
#     brand = request.form['brand']
#     model = request.form['model']
#     cost = request.form['cost']
#     cleanTitle = request.form['cleanTitle']
#     notes = request.form['notes']
#     images = request.files['images']

#     print(year)
#     print(brand)
#     print(model)
#     print(cost)
#     print(cleanTitle)
#     print(notes)
#     # print(images.filename)
    
#     # for img in images:
#     #   print(img)
    
#     return 'Success'
#     # return json.dumps({'brand': 'brand'})