#!/usr/bin/python

from flask import *
from pub import *
from setup import *

@app.route("/login", methods = ['GET','POST'])

def login():
	if request.method == 'GET':
		return render_template('login.html')
	if request.method == 'POST':
		usern = request.form['username']
		passw = request.form['password']
		
		if User.query.filter_by(username = usern).first():
			if User.query.filter_by(password = passw).first():
				flash('Successful login.')
				session['username'] = usern
				return redirect(url_for('layout'))
			else:
				error = 'Invalid Password.'
		else:
			error = 'Invalid Username.'

		return render_template('login.html', error = error)

@app.route("/", methods = ['GET','POST'])

def layout():
	if request.method == 'GET':
		if 'username' in session:
			return render_template('layout.html')
		else:
			return redirect(url_for('login'))
	if request.method == 'POST':
		content = request.form['content']
		preview = request.form['preview']

		if not content:
			return 'Content Empty.'
		else:
			post = Post(content)
			db.session.add(post)
			db.session.commit()
		
		return 'Pubbed'
		#if preview == 'True':
		#	return publish(content, True)
		#return publish(content, False)

for blog in Blog.query.all():
	@app.route("/" + str(blog), methods = ['GET'])

	def index():
		return render_template('index.html', blogtitle='hi', posts = Post.query.all())

@app.route("/preview")

def show_preview():
	return render_template('preview.html')

@app.route("/pubbed")

def show_pubbed():
	return render_template('layout.html')

@app.errorhandler(404)
def not_found(error):
	return redirect('https://www.google.co.in/search?q=404')

if __name__ == "__main__":
	app.run(debug = True)