import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

url = os.getenv("DATABASE_URL")
if url is None:
    url = os.getenv("DATABASE_URL_AUTH")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
