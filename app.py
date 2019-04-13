import os
from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__, static_folder='./images')
# dialect+driver://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/test'
db = SQLAlchemy(app)
CORS(app)

@app.route('/')
def index():
  return 'index'

class CarInformation(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  year = db.Column(db.Numeric(precision=4, asdecimal=False, decimal_return_scale=None))
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

class CarExpenses(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  carInformationId = db.Column(db.Numeric(asdecimal=False, decimal_return_scale=None))
  cost = db.Column(db.String(50))
  expense = db.Column(db.String(120))

  def __init__(self, carInformationId, cost, expense):
    self.carInformationId = carInformationId
    self.cost = cost
    self.expense = expense

@app.route('/upload', methods=['POST', 'GET'])
def upload():
  if request.method == 'POST':
    year = request.form['year']
    brand = request.form['brand']
    model = request.form['model']
    cost = request.form['cost']
    cleanTitle = request.form['cleanTitle']
    notes = request.form['notes']

    if cleanTitle == 'true':
      cleanTitle = True
    elif cleanTitle == 'false': 
      cleanTitle = False

    CarInfo = CarInformation(year, brand, model, cost, cleanTitle, notes)
    db.session.add(CarInfo)
    db.session.commit()

    lastCarInfoId = CarInformation.query.order_by(CarInformation.id.desc()).first().id
    os.makedirs('./images/cars/{}'.format(lastCarInfoId))
    for img in request.files:
      request.files[img].save('./images/cars/{}/{}'.format(lastCarInfoId, request.files[img].filename))

    return 'Success'

  elif request.method == 'GET':
    cars = CarInformation.query.all()
    result = []
    for row in cars:
      location = {}
      location['id'] = row.id
      location['year'] = int(row.year)
      location['brand'] = row.brand
      location['model'] = row.model
      location['cost'] = row.cost
      location['cleanTitle'] = row.cleanTitle
      location['notes'] = row.notes
      car_list = []
      cars_directory = os.listdir('./images/cars/{}'.format(row.id))
      for link in cars_directory:
          car_list.append('./images/cars/{}/{}'.format(row.id, link))
      location['images'] = car_list
      result.append(location)

    return json.dumps(result)

@app.route('/carinfo/<int:carId>')
def loadCarDetails(carId):
  carInfo = CarInformation.query.get(carId)
  car = {
    'year': carInfo.year,
    'brand': carInfo.brand,
    'model': carInfo.model,
    'cost': carInfo.cost,
    'cleanTitle': carInfo.cleanTitle,
    'notes': carInfo.notes,
  }

  return json.dumps(car)

@app.route('/carimages/<int:carId>')
def loadCarImages(carId):
  carImages = {
    'images': []
  }
  cars_directory = os.listdir('./images/cars/{}'.format(carId))
  for link in cars_directory:
      carImages['images'].append('./images/cars/{}/{}'.format(carId, link))

  return json.dumps(carImages)


@app.route('/createexpense/<int:carId>', methods=['POST'])
def createExpense(carId):
  carInformationId = carId
  cost = request.form['cost']
  expense = request.form['expense']

  CarExpense = CarExpenses(carInformationId, cost, expense)
  db.session.add(CarExpense)
  db.session.commit()
  return 'Success'

@app.route('/updateexpense/<int:expenseId>', methods=['POST'])
def updateExpense(expenseId):
  cost = request.form['cost']
  expense = request.form['expense']

  CarExpense = CarExpenses.query.get(expenseId)
  CarExpense.cost = cost
  CarExpense.expense = expense

  db.session.commit()

  return 'Success'

@app.route('/loadexpenses/<int:carId>')
def loadExpenses(carId):
  carExpense = CarExpenses.query.filter_by(carInformationId=carId).all()
  result = []

  for row in carExpense:
    result.append({
      'expenseId': row.id,
      'carInformationId': int(row.carInformationId),
      'cost': row.cost,
      'expense': row.expense,
    })

  return json.dumps(result)

@app.route('/deleteexpense/<int:expenseId>', methods=['POST'])
def deleteExpense(expenseId):
  print('expenseId', expenseId)
  carExpenseId = CarExpenses.query.get(expenseId)
  db.session.delete(carExpenseId)
  db.session.commit()

  return 'Success'

@app.route('/updatecarinfo/<int:carId>', methods=['POST'])
def updateCarInfo(carId):
  year = request.form['year']
  brand = request.form['brand']
  model = request.form['model']
  cost = request.form['cost']
  cleanTitle = request.form['cleanTitle']
  notes = request.form['notes']

  if cleanTitle == 'true':
    cleanTitle = True
  elif cleanTitle == 'false': 
    cleanTitle = False

  carInfo = CarInformation.query.get(carId)

  carInfo.year = int(year)
  carInfo.brand = brand
  carInfo.model = model
  carInfo.cost = cost
  carInfo.cleanTitle = cleanTitle
  carInfo.notes = notes

  db.session.commit()

  # session.query().filter(carInfo.brand == 'test').update({"no_of_logins": (User.no_of_logins +1)})
  # session.commit()

  # carInfo = CarInformation.query.filter_by(carId=carId)
  # db.session.update({"nameOfRow??": 'value'})
  # session.commit()
  # session.query().filter(User.username == form.username.data).update({"no_of_logins": (User.no_of_logins +1)})
  return 'hi'


@app.route('/deleteimage', methods=['POST'])
def deleteImage():
  imagePath = request.form['path']
  folderPath = imagePath.rsplit('/', 1)[0]
  dirContents = os.listdir(folderPath)

  if len(dirContents) == 1:
    print('Cant remove if only one image')
  elif len(dirContents) == 0:
    os.rmdir(folderPath)
  else:
    os.remove(imagePath)

  return 'test'

@app.route('/deleteCar/<int:carId>', methods=['POST'])
def deleteCar(carId):
  carExpense = CarExpenses.query.filter_by(carInformationId=carId).all()
  for row in carExpense:
    db.session.delete(row)
  
  carInfo = CarInformation.query.get(carId)
  db.session.delete(carInfo)
  db.session.commit()

  cars_directory = os.listdir('./images/cars/{}'.format(carId))
  for link in cars_directory:
    print('./images/cars/{}/{}'.format(carId, link))
    os.remove('./images/cars/{}/{}'.format(carId, link))

  os.rmdir('./images/cars/{}'.format(carId))

  return 'test'