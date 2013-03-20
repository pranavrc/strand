from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
import os
import sys

app = Flask(__name__, template_folder = 'templates')

DB_URI = 'tmp/data.db'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, DB_URI)
app.secret_key = ';HX)JW&FD;pN~G+EBRkPuXg}Hw><h9-7hBd&:9b!n|:HGQ*I,+Bc:Z6xmC V=|CQ'
db = SQLAlchemy(app)

class Footer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    footerContent = db.Column(db.PickleType)

    def __init__(self, footerContent):
        self.footerContent = footerContent

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True)
    password = db.Column(db.String(100), unique = False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '%r' % self.username

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)
    blog_url = db.Column(db.Text, db.ForeignKey('blog.url'))

    def __init__(self, body, blog_url, pub_date = None):
        self.body = body
        self.blog_url = blog_url
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date

    def __repr__(self):
        return '%r' % self.body

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text)
    url = db.Column(db.String(100), unique = True)
    description = db.Column(db.Text)
    bloglayout = db.Column(db.Boolean, unique = False)
    posts = db.relationship('Post', backref = 'blog', lazy = 'dynamic')

    def __init__(self, title, url, bloglayout, description):
        self.title = title
        self.url = url
        self.bloglayout = bloglayout
        self.description = description

    def __repr__(self):
        return '%r' % self.url
