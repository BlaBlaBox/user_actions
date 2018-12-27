import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

url = os.getenv("DATABASE_URL")
if url is None:
    url = os.getenv("DATABASE_URL_AUTH")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


# For local testing
# "postgres://jgvykwkfupxdri:15370819400d0b8df8b5ea1ab634f31be1631dd5112298a341af4dfea7eed19c@ec2-54-246-90-194.eu-west-1.compute.amazonaws.com:5432/d4ort64q3gmkjd"
