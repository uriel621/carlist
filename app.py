import os
from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pymysql
from PIL import Image

import sys
print('Python Version--->', sys.version)

pymysql.install_as_MySQLdb()

app = Flask(__name__, static_folder='./images')
# basedir = os.path.abspath(os.path.dirname(__file__))

# # FOR SERVER
# server_path = '/home/uriel621/be-carlist/images/cars'
# appended_link = 'http://uriel.sellingcrap.com/images/cars'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://uriel621:mercerst.13@uriel621.mysql.pythonanywhere-services.com/uriel621$cars'

# FOR BlueHost
server_path = './images/cars'
appended_link = 'https://be-carlist.herokuapp.com/images/cars'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hzmnrnmy_uriel:mercerst.13@50.87.249.228:3306/hzmnrnmy_carlist'

# # FOR DEV
# # Azure Credentials
# account = app.config['ACCOUNT'] = 'carimages621'
# key = app.config['STORAGE_KEY'] = '9roKuaNkbwS0dShYe8/PiyQL4De1vlHDjLihdXH5UsfBC0XXhwxKtrGxTYX2IP7s9xUOAv+s4d7z3IptTyDM9A=='
# container = app.config['CONTAINER'] = 'cars'

# server_path = './images/cars'
# appended_link = 'http://localhost:5000/images/cars'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/carlist'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app, supports_credentials=True)

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
  sold = db.Column(db.Boolean, default=False)
  priceSold = db.Column(db.String(50), default=0)
  yearSold = db.Column(db.Integer)
  partner = db.Column(db.String(50))

  def __init__(self, year, brand, model, cost, cleanTitle, notes, sold, priceSold, yearSold, partner):
    self.year = year
    self.brand = brand
    self.model = model
    self.cost = cost
    self.cleanTitle = cleanTitle
    self.notes = notes
    self.sold = sold
    self.yearSold = yearSold
    self.partner = partner

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
    partner = request.form['partner']

    if cleanTitle == 'true':
      cleanTitle = True
    elif cleanTitle == 'false':
      cleanTitle = False

    if partner != 'admin' and partner != 'Omar' and partner != 'David':
      return 'DENIED'

    sold = False
    priceSold = '0'
    yearSold = 0
  
    CarInfo = CarInformation(year, brand, model, cost, cleanTitle, notes, sold, priceSold, yearSold, partner)
    db.session.add(CarInfo)
    db.session.commit()

    lastCarInfoId = CarInformation.query.order_by(CarInformation.id.desc()).first().id

    path = '{}/{}'.format(server_path, lastCarInfoId)
    os.makedirs(path)


    for img in request.files:
      im = Image.open(request.files[img])
      request.files[img].filename = '{}-{}'.format(img, request.files[img].filename)
      saved_path = '{}/{}/{}'.format(server_path, lastCarInfoId, request.files[img].filename)
      FixImage(im).save(saved_path, optimize=True, quality=25)

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
      cars_directory = os.listdir('{}/{}'.format(server_path, row.id))
      for link in cars_directory:
          car_list.append('{}/{}/{}'.format(appended_link, row.id, link))
      location['images'] = car_list
      result.append(location)

    return json.dumps(result)

@app.route('/fetchcars', methods=['GET'])
def fetchcars():
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
    cars_directory = os.listdir('{}/{}'.format(server_path, row.id))
    for link in cars_directory:
        car_list.append('{}/{}/{}'.format(appended_link, row.id, link))
    location['images'] = car_list
    result.append(location)

  return json.dumps(result)

@app.route('/uploadcar', methods=['POST'])
def uploadcar():
  year = request.form['year']
  brand = request.form['brand']
  model = request.form['model']
  cost = request.form['cost']
  cleanTitle = request.form['cleanTitle']
  notes = request.form['notes']
  partner = request.form['partner']

  if cleanTitle == 'true':
    cleanTitle = True
  elif cleanTitle == 'false':
    cleanTitle = False

  if partner != 'admin' and partner != 'Omar' and partner != 'David':
    return 'DENIED'

  sold = False
  priceSold = '0'
  yearSold = 0

  CarInfo = CarInformation(year, brand, model, cost, cleanTitle, notes, sold, priceSold, yearSold, partner)
  db.session.add(CarInfo)
  db.session.commit()

  lastCarInfoId = CarInformation.query.order_by(CarInformation.id.desc()).first().id

  path = '{}/{}'.format(server_path, lastCarInfoId)
  os.makedirs(path)


  for img in request.files:
    im = Image.open(request.files[img])
    request.files[img].filename = '{}-{}'.format(img, request.files[img].filename)
    saved_path = '{}/{}/{}'.format(server_path, lastCarInfoId, request.files[img].filename)
    FixImage(im).save(saved_path, optimize=True, quality=25)

  return 'Success'

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
    'partner': carInfo.partner
  }

  return json.dumps(car)

@app.route('/carimages/<int:carId>')
def loadCarImages(carId):
  carImages = {
    'images': []
  }
  cars_directory = os.listdir('{}/{}'.format(server_path, carId))
  for link in cars_directory:
      carImages['images'].append('{}/{}/{}'.format(appended_link, carId, link))

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
  partner = request.form['partner']

  if cleanTitle == 'true':
    cleanTitle = True
  elif cleanTitle == 'false':
    cleanTitle = False

  carInfo = CarInformation.query.get(carId)
  print('carInfo--->>>', carInfo)
  carInfo.year = int(year)
  carInfo.brand = brand
  carInfo.model = model
  carInfo.cost = cost
  carInfo.cleanTitle = cleanTitle
  carInfo.notes = notes
  carInfo.partner = partner

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

  cars_directory = os.listdir('{}/{}'.format(server_path, carId))
  for link in cars_directory:
    os.remove('{}/{}/{}'.format(server_path, carId, link))

  os.rmdir('{}/{}'.format(server_path, carId))

  return 'test'

@app.route('/carstatus/<int:carId>')
def carStatus(carId):
  carInfo = CarInformation.query.get(carId)

  carStatus = {
    'sold': carInfo.sold,
    'partner': carInfo.partner,
    'priceSold': carInfo.priceSold,
    'yearSold': carInfo.yearSold,
  }

  return json.dumps(carStatus)


@app.route('/updatecarstatus/<int:carId>', methods=['POST'])
def updateCarStatus(carId):
  price_sold = request.json['priceSold']
  year_sold = request.json['yearSold']
  sold_status = request.json['soldStatus']
  
  carInfo = CarInformation.query.get(carId)

  if bool(sold_status) == False:
    carInfo.sold = False
    carInfo.yearSold = 0
    carInfo.priceSold = 0
  else:
    carInfo.sold = True
    if bool(year_sold) == True:
      carInfo.yearSold = int(year_sold)
    if bool(price_sold) == True:
      carInfo.priceSold = int(price_sold)

  db.session.commit()
  return 'test'

@app.route('/authenticate', methods=['POST'])
def authenticate():
  code = request.json['code']
  code = ''.join(str(e) for e in code)
  print('code-->>', code)

  authenticate = False
  if code == '1122':
    authenticate = 'admin'
  elif code == '0123': 
    authenticate = 'Omar'
  elif code == '4444':
    authenticate = 'David'

  return json.dumps(authenticate)



@app.route('/uploadimages/<int:carId>', methods=['POST'])
def uploadImages(carId):
  for img in request.files:
    print(request.files[img].filename)
    im = Image.open(request.files[img])
    request.files[img].filename = '{}-{}'.format(img, request.files[img].filename)
    saved_path = '{}/{}/{}'.format(server_path, carId, request.files[img].filename)
    FixImage(im).save(saved_path, optimize=True, quality=25)

  return 'ji'


@app.route('/makemainimage', methods=['POST'])
def makeMainImage():
  currentMain = request.json['currentMain']
  newMain = request.json['newMain']

  newIndex = newMain.rindex('/')

  firstHalf = newMain[:newIndex + 1]
  lastHalf = newMain[newIndex + 2:]

  newPath = newMain[newIndex + 1:].index('-')
  newPath = newMain[newIndex + 1:][:newPath]
  newMain = '{}0{}'.format(firstHalf, lastHalf)


  newIndex = currentMain.rindex('/')
  firstHalf = currentMain[:newIndex + 1]
  lastHalf = currentMain[newIndex + 2:]

  currentMain = '{}{}{}'.format(firstHalf, newPath, lastHalf)


  # olc = './'.format(request.json['newMain'])
  # olcz = './'.format(newMain)
  # olm = './'.format(request.json['currentMain'])
  # olmz = './'.format(currentMain)
  os.rename('./{}'.format(request.json['newMain']), './{}'.format(newMain))
  os.rename('./{}'.format(request.json['currentMain']), './{}'.format(currentMain))
  # print('firstHalf', firstHalf)
  # print('lastHalf', lastHalf)
  # print('newPath', newPath)



  # print('newIndex', newIndex)
  # print('other', other)

  return '???'

@app.route('/fetchpartners', methods=['GET'])
def fetchPartners():
  # cars = CarInformation.query.all()
  # partners = []
  # for row in cars:
  #   if row.partner not in partners:
  #     partners.append(row.partner)

  partners = [
    'admin',
    'Omar',
    'David'
  ]

  return json.dumps(partners)

def FixImage(img, max_width=None, max_height=None):
  '''
  Strips an image of everything but its basic data (nasty EXIF tags, gif animations, etc.), first correcting orientation if necessary.

  'img' must be a PIL.Image.Image instance. Returns a new instance. Requires the PIL.Image (Python Image Library) or equivalent to be imported as Image; image formats supported depend on PIL prereqs installed on the system (see http://pillow.readthedocs.io/en/3.0.x/installation.html).

  If max_width and/or max_height are supplied (pixels as int), the image is proportionally downsized to fit the tighter of the two constraints using a high-quality downsampling filter.
  '''

  ORIENT = { # exif_val: (rotate degrees cw, mirror 0=no 1=horiz 2=vert); see http://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/EXIF.html
            2: (0, 1),
            3: (180, 0),
            4: (0, 2),
            5: (90, 1),
            6: (270, 0),
            7: (270, 1),
            8: (90, 0),
            }

  assert isinstance(img, Image.Image), "Invalid 'img' parameter to fix_image()"
  img_format = img.format

  # fix img orientation (issue with jpegs taken by cams; phones in particular):
  try:
      orient = img._getexif()[274]
  except (AttributeError, KeyError, TypeError, ValueError):
      orient = 1 # default (normal)
  if orient in ORIENT:
      (rotate, mirror) = ORIENT[orient]
      if rotate:
          img = img.rotate(rotate)
      if mirror == 1:
          img = img.transpose(Image.FLIP_LEFT_RIGHT)
      elif mirror == 2:
          img = img.transpose(Image.FLIP_TOP_BOTTOM)

  # strip image
  data = img.getdata()
  palette = img.getpalette()
  img = Image.new(img.mode, img.size)
  img.putdata(data)
  if palette:
      img.putpalette(palette)

  # resize image (if necessary):
  (width, height) = img.size
  if max_width and width > max_width and (not max_height or width*max_height >= height*max_width): # width is constraint
      img = img.resize((max_width, round(height*max_width/width)), Image.LANCZOS)
  elif max_height and height > max_height: # height is constraint
      img = img.resize((round(width*max_height/height), max_height), Image.LANCZOS)

  img.format = img_format # preserve orig format
  return img

if __name__ == "__main__": # run this script as-is for a basic test
  # *****************
  # * Usage Example *
  # *****************
  infile = input('Input image filename: ')
  try:
      img = Image.open(infile)
  except IOError as err:
      print('Error opening file:', str(err))
      img = None
  if img:
      if img.format:
          print('Image format:', img.format) # use in Content-Type: image/format header when returning image over the web)
          outfile = input('Output image filename: ')
          max_width = int(input('New max width (0 for none): '))
          max_height = int(input('New max height (0 for none): '))

          FixImage(img, max_width, max_height).save(outfile, img.format)
          # alternatively, to get the image binary instead of writing it back to a file (python3):
          # > from io import BytesIO
          # > new_img = BytesIO()
          # > FixImage(img, max_width, max_height).save(new_img, img.format)
          # > new_image_binary = new_img.getvalue()
          print('New image saved.')
      else:
          print('Unrecognized image format.')