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

@app.route("/add", methods = ['GET','POST'])

def addPage():
	if request.method == 'GET':
		return render_template('addpage.html')
	if request.method == 'POST':
		blogurlinput = request.form['blogurlinput']

		if not blogurlinput:
			return render_template('addpage.html', added = 'URL cannot be empty')

		if Blog.query.filter_by(url = blogurlinput).first():
			return render_template('addpage.html', added = 'Page exists.')

		blogtitleinput = request.form['blogtitleinput']
		blogdescinput = request.form['blogdescinput']
		bloglayoutinput = request.form['bloglayoutinput']
		db.session.add(Blog(blogtitleinput, blogurlinput, bloglayoutinput, blogdescinput))
		db.session.commit()
		return render_template('addpage.html', added = blogurlinput)

@app.route("/remove", methods = ['GET', 'POST'])

def removePage():
	if request.method == 'GET':
		return render_template('removepage.html', blogs = Blog.query.all())
	if request.method == 'POST':
		blogtoremove = request.form['blogtoremove']
		db.session.delete(Blog.query.filter_by(url = blogtoremove).first())
		db.session.commit()
		return render_template('removepage.html', blogs = Blog.query.all(), removed = blogtoremove)

@app.route("/", methods = ['GET','POST'])

def layout():
	if request.method == 'GET':
		if 'username' in session:
			return render_template('layout.html', blogs = Blog.query.all())
		else:
			return redirect(url_for('login'))
	if request.method == 'POST':
		content = request.form['content']
		preview = request.form['preview']
		blogtopostto = request.form['listofblogs']

		if str(preview) == 'True':
			preview = False
			return render_template('preview.html', body = content, pub_date = datetime.utcnow())

		blog = Blog.query.filter_by(url = blogtopostto).first()
		post = Post(content, blog.url)
		db.session.add(post)
		db.session.commit()

		return '<a href="%s" target="_blank">Published</a>' % url_for('index', blogurl = blogtopostto)

@app.route("/<blogurl>", methods = ['GET'])

def index(blogurl):
	if not Blog.query.filter_by(url = blogurl).first():
		return redirect('https://www.google.com/search?q=404')

	eachblog = Blog.query.filter_by(url = blogurl).first()
	contentPosts = eachblog.posts.all()

	if eachblog.bloglayout:
		contentPosts.reverse()

	return render_template('index.html', blogtitle = eachblog.title, blogdescription = eachblog.description, posts = contentPosts)

@app.errorhandler(404)

def not_found(error):
	return redirect('https://www.google.com/search?q=404')

@app.teardown_request

def shutdown_session(exception=None):
    db.session.remove()

if __name__ == "__main__":
	app.run(debug = True)
