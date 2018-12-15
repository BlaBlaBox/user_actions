from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from ua_config import app

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

    def __init__(self, **kwargs):
        self.__dict__ = self
        super().__init__(**kwargs)


def add_person(name, surname, gender, dob):

    new_person = Person(firstname=name, surname=surname, gender=gender, dob=dob)
    db.session.add(new_person)
    db.session.commit()
    return new_person


def signUp(name, surname, gender, dob, username, pass_hash, email):
    new_person = add_person(name, surname, gender, dob)
    p_id = new_person.person_id

    new_user = User(person_id=p_id, username=username, pass_hash=pass_hash, mail=email)
    db.session.add(new_user)
    db.session.commit()
    return new_user


def getPasshashFromEmail(email):
    return User.query.filter_by(mail=email).first().pass_hash


def checkUsername(username):
    return User.query.filter_by(username=username).first()


def checkMail(email):
    return User.query.filter_by(mail=email).first()


def updateUser(user_id, name, surname, gender, dob, username, pass_hash, email):
    user_obj = User.query.filter_by(user_id=user_id).first()
    p_id = user_obj.person_id
    user_obj.username = username
    user_obj.pass_hash = pass_hash
    user_obj.email = email

    db.session.commit()

    person_obj = Person.query.filter_by(person_id=p_id).first()
    person_obj.name = name
    person_obj.surname = surname
    person_obj.gender = gender
    person_obj.dob = dob

    db.session.commit()

    return user_obj


def getPassHash(uname_mail, is_mail):
    if is_mail:
        return User.query.filter_by(mail=uname_mail).first().pass_hash
    return User.query.filter_by(username=uname_mail).first().pass_hash


def getAllUsers():
    return User.query.all()


def getUser(user_id):
    return User.query.filter_by(user_id=user_id).first()


def changeActiveState(user_id):
    user_obj = User.query.filter_by(user_id=user_id).first()
    user_obj.is_active = not user_obj.is_active
    db.session.commit()
    return user_obj.is_active


db.create_all()
