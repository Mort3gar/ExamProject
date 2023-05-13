from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

db = SQLAlchemy(app)
db_metadata = db.metadata

from app import routes, models
db.create_all()