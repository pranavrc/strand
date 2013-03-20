from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from models import *
import os

class Data:
    def __init__(self):
        self.username = str(raw_input("Enter your username: "))
        self.password = str(raw_input("Enter your password: "))
        self.footerLinks = {}
        linkCount = 0

        while True:
            self.confPass = str(raw_input("Confirm your password: "))
            if self.confPass == self.password:
                break

        self.title = str(raw_input("Blog title? "))
        self.desc = str(raw_input("Blog Description? "))
        self.blogurl = str(raw_input("Blog URL Name? Eg: strand (http://yourdomain.com/strand/) "))

        self.layout = str(raw_input("Bottom-to-Top (press y) or Top-to-Bottom (press n)? (Default: Bottom to Top) "))

        if self.layout == 'n':
            self.layout = 0
        else:
            self.layout = 1

        footer = str(raw_input("Need Footer links? (y(default)/n) "))
        if footer == 'n':
            pass
        else:
            linkCount = int(raw_input("How many? "))
            for count in range(linkCount):
                caption = str(raw_input("Caption: "))
                link = str(raw_input("Hyperlink: "))
                self.footerLinks[caption] = link

if __name__ == "__main__":
    if os.path.exists(DB_URI):
        confirm = str(raw_input("User Database exists already. Do you want to re-configure? This will erase your current database configuration. Confirm (y/n) "))
        while True:
            if confirm == 'y' or confirm == 'Y':
                db.drop_all()
                break
            elif confirm == 'n' or confirm == 'N':
                sys.exit(1)
            else:
                confirm = str(raw_input('Press y or n. '))
                continue

    a = Data()
    db.create_all()
    user = User(a.username, a.password)
    db.session.add(user)
    blog = Blog(a.title, a.blogurl, a.layout, a.desc)
    db.session.add(blog)
    footer = Footer(a.footerLinks)
    db.session.add(footer)
    db.session.commit()
    abc = User.query.all()
