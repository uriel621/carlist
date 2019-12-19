install

pip install flask
pip install flask_sqlalchemy
pip install flask_cors
pip install pymysql

Create database in mysql shell
  >CREATE DATABASE test
  >SHOW DATABASES

Create model in python shell
  >from app import db
  >db.create_all()

  http://flask-sqlalchemy.pocoo.org/2.3/queries/#querying-records

  update
  There are several ways to UPDATE using sqlalchemy

  1) user.no_of_logins += 1
    session.commit()

  2) session.query().\
        filter(User.username == form.username.data).\
        update({"no_of_logins": (User.no_of_logins +1)})
    session.commit()

  3) conn = engine.connect()
    stmt = User.update().\
        values(no_of_logins=(User.no_of_logins + 1)).\
        where(User.username == form.username.data)
    conn.execute(stmt)

  4) setattr(user, 'no_of_logins', user.no_of_logins+1)
    session.commit()

  pip freeze > requirements.txt

   heroku git:remote -a be-carlist
   git push heroku master