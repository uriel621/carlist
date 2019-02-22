from flask import Flask, json, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'index'

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    car_name = request.form['car_name']
    brand = request.form['brand']
    year = request.form['year']
    clean = request.form['clean']
    filez = request.files['file']
    print(dir(filez))

    # print(request.files['file'].filename)
    # print(request.files['file'].size)
    # print(request.files['file'].filename)

    # filez.save('./images/uploaded_file.jpg')

    # print(car_name)
    # print(brand)
    # print(year)
    # print(clean)
    return 'Success'
    # return json.dumps({'brand': 'brand'})