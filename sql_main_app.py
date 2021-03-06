import os
from flask import Flask, flash, redirect, render_template, request, session, abort
from gevent.pywsgi import WSGIServer
import g_images_download  # importing the library
import g_images_download  # importing the library
from random import randint
import random

from flask_sqlalchemy import SQLAlchemy


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

response = g_images_download.googleimagesdownload()  # class instantiation
arguments = {"keywords": "cat", "no_download": "no_download", "limit": 10}  # creating list of arguments


class Book(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    #url = db.Column(db.String(300), unique=True, nullable=True, primary_key=False)

    def __repr__(self):
        return "<Title: {}>".format(self.title)


@app.route("/", methods=['GET', 'POST'])
def index():
    books = Book.query.all()
    if request.method == "POST":
        text = request.form['text']
        if text == "":
            text = "cat"
        arguments["keywords"] = text
        book = Book(title = text)

	books = Book.query.all()
	if (text not in books):
		# adding the text to the DB
		db.session.add(book)
		db.session.commit()

    
    	print(books)

    return render_template('index.html', books=books)


@app.route("/img", methods=['GET', 'POST'])
def img():
    paths, img_list = response.download(arguments)  # passing the arguments to the function
    return update_content(img_list)


def img_get(img_list):
    f = open("saving_the_urls.txt", "r").read().splitlines()
    img_url = random.choice(f)
    return img_url


def update_content(img_list):
    # random.choice(img_list)
    imgs = random.sample(img_list, 3)
    # print(img1)

    return render_template('test.html', name1=imgs[0], name2=imgs[1], name3=imgs[2])


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8001)


