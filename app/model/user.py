from flask_sqlalchemy import SQLAlchemy
from ..app import db
db = SQLAlchemy(app)
class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    password = db.Column(db.String)
    