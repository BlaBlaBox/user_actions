import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


url = os.getenv("DATABASE_URL")
if url is None:
    print("Usage: DATABASE_URL=url python ua_config.py", file=sys.stderr)
    sys.exit(1)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
