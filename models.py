from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
import os
import sys

app = Flask(__name__, template_folder = 'templates')

DB_URI = 'tmp/data.db'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, DB_URI)
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(80), unique = True)
	password = db.Column(db.String(100), unique = False)
	
	def __init__(self, username, password):
		self.username = username
		self.password = password

	def __repr__(self):
		return '<User %r>' % self.username

class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.Text)
	pub_date = db.Column(db.DateTime)

	def __init__(self, body, pub_date = None):
		self.body = body
		if pub_date is None:
			pub_date = datetime.utcnow()
		self.pub_date = pub_date

	def __repr__(self):
		return '<Post %r>' % self.body
