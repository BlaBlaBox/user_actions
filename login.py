from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://blablabox:passw@localhost:5432/authentication'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Person(db.Model):

    person_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(1))
    dob = db.Column(db.Date)


class User(db.Model):

    person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    pass_hash = db.Column(db.String(87), nullable=False)
    mail = db.Column(db.String(50), unique=True, nullable=False)
    register_date = db.Column(db.DateTime, default=(datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)


def getPasshashFromEmail(email):
    return User.query.filter_by(mail=email).first().pass_hash




db.create_all()