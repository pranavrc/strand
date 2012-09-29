#!/usr/bin/python

from flask import *
from pub import *
from setup import app

@app.route("/login", methods = ['GET','POST'])

def login():
	if request.method == 'GET':
		return render_template('login.html')
	if request.method == 'POST':
		return 'foo'

@app.route("/", methods = ['GET','POST'])

def index():
	if request.method == 'GET':
		return render_template('layout.html')
	if request.method == 'POST':
		content = request.form['content']
		preview = request.form['preview']
		if preview == 'True':
			return publish(content, True)
		return publish(content, False)

@app.route("/preview")

def show_preview():
	return render_template('preview.html')

@app.route("/pubbed")

def show_pubbed():
	return render_template('index.html')

if __name__ == "__main__":
	app.run(debug = True)
