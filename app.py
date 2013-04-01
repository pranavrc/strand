#!/usr/bin/python

from flask import *
from pub import *
from setup import *
import re
import os

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

@app.route("/logout", methods = ['GET', 'POST'])

def logout():
    if request.method == 'GET':
        if 'username' in session:
            del session['username']

        return redirect(url_for('login'))

@app.route("/add", methods = ['GET','POST'])

def addPage():
    if request.method == 'GET':
        if 'username' in session:
            return render_template('addpage.html')
        else:
            return redirect(url_for('login'))
    if request.method == 'POST':
        medium = custompost()

        if 'username' in session or medium:
            blogurlinput = request.form['blogurlinput']

            if not blogurlinput or not regmatch(blogurlinput):
                return render_template('addpage.html', added = 'Invalid URL. Cannot contain special characters other than underscore.')

            if Blog.query.filter_by(url = blogurlinput).first():
                return render_template('addpage.html', added = 'Page exists.')

            blogtitleinput = request.form['blogtitleinput']
            blogdescinput = request.form['blogdescinput']
            bloglayoutinput = request.form['bloglayoutinput']
            db.session.add(Blog(blogtitleinput, blogurlinput, bloglayoutinput, blogdescinput))
            db.session.commit()

            if not medium:
                return render_template('addpage.html', added = blogurlinput)
            else:
                return 'Added.'
        else:
            return redirect(url_for('login'))

@app.route("/remove", methods = ['GET', 'POST'])

def removePage():
    if request.method == 'GET':
        if 'username' in session:
            return render_template('removepage.html', blogs = Blog.query.all())
        else:
            return redirect(url_for('login'))
    if request.method == 'POST':
        medium = custompost()

        if 'username' in session or medium:
            blogtoremove = request.form['blogtoremove']
            db.session.delete(Blog.query.filter_by(url = blogtoremove).first())
            db.session.commit()

            if not medium:
                return render_template('removepage.html', blogs = Blog.query.all(), removed = blogtoremove)
            else:
                return 'Removed.'
        else:
            return redirect(url_for('login'))

@app.route("/", methods = ['GET','POST'])

def layout():
    if request.method == 'GET':
        if 'username' in session:
            return render_template('layout.html', blogs = Blog.query.all())
        else:
            return redirect(url_for('login'))
    if request.method == 'POST':
        medium = custompost()

        if 'username' in session or medium:
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

            if not medium:
                return '<a href="%s" target="_blank">Published</a>' % url_for('index', blogurl = blogtopostto)
            else:
                return 'Published.'
        else:
            return '<a href="%s">Login.</a>' % url_for('login')

@app.route("/<blogurl>", methods = ['GET'])

def index(blogurl):
    if not Blog.query.filter_by(url = blogurl).first():
        return redirect('https://www.google.com/search?q=404')

    eachblog = Blog.query.filter_by(url = blogurl).first()
    contentPosts = eachblog.posts.all()
    footer = Footer.query.all()[0]

    if eachblog.bloglayout:
        contentPosts.reverse()

    return render_template('index.html', blogtitle = eachblog.title, blogdescription = eachblog.description, posts = contentPosts, \
                            footerContent = footer.footerContent)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploads', methods = ['GET', 'POST'])

def uploads():
    if request.method == 'GET':
        if 'username' in session:
            return render_template('uploads.html', uploadList = os.listdir(app.config['UPLOAD_FOLDER']))
        else:
            return redirect(url_for('login'))
    if request.method == 'POST':
        uploadContent = request.files['file']
        if uploadContent and allowed_file(uploadContent.filename):
            filename = secure_filename(uploadContent.filename)
            uploadContent.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploads', filename = filename))

@app.route('/uploads/<filename>', methods = ['GET'])

def uploadedContent(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/remove/<filename>', methods = ['GET'])

def removeContent(filename):
    if 'username' in session:
        os.remove('uploads/' + filename)
        return redirect(url_for('uploads'))
    else:
        return redirect(url_for('login'))

@app.errorhandler(404)

def not_found(error):
    return redirect('https://www.google.com/search?q=404')

@app.teardown_request

def shutdown_session(exception=None):
    db.session.remove()

def regmatch(urlinput, isPresent = re.compile(r'[^a-z0-9_]').search):
    return not bool(isPresent(urlinput))

def custompost():
    medium = True

    try:
        if User.query.filter_by(password = request.form['password']).first():
            pass
        else:
            medium = False
    except:
        medium = False

    return medium

if __name__ == "__main__":
    app.run(debug = True)
