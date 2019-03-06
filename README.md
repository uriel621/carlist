install

pip install flask
pip install flask_sqlalchemy
pip install flask_cors
pip install pymysql

Create database in mysql shell
  >>>CREATE DATABASE test
  >>>SHOW DATABASES

Create model in python shell
  >>>from app import db
  >>>db.create_all() 