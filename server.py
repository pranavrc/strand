#!/usr/bin/python

from flask import *
from pub import *

app = Flask(__name__)

@app.route("/", methods = ['GET','POST'])

def index():
	if request.method == 'GET':
		return render_template('index.html')
	if request.method == 'POST':
		content = request.form['content']
		return publish(content)

if __name__ == "__main__":
	app.run(debug = True)
