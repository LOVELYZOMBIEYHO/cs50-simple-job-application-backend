\*\*\* Heroku Must not use Sqlite because of Dyno of Heroku (The data will be deleted automatically),should use Postgresql.

Python version 3.10.0

URL:https://cs50-simple-job-application.herokuapp.com/
-Create an environment

> mkdir myproject
> cd myproject
> py -3 -m venv venv

-Activate the environment

> venv\Scripts\activate

-Deactivate the environment

> deactivate

-Debug mode (powershell)
$env:FLASK_ENV = "development"

-Create database (with SQLAlchemy) "\*"= "\_"

import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(**name**)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(app.root_path,"sqlite.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
id = db.Column(db.Integer, primary_key=True)
username = db.Column(db.String(80), unique=True, nullable=False)
email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

-Use "flask shell" to commend mode and type:

> from app import db
> db.create_all()

-Record all modules or plugins in requirement.txt

> pip freeze > requirements.txt

---

PDFKIT on Heroku (important when deploy Heroku app)

https://www.nuanced.it/2018/05/using-pdfkit-on-heroku.html

Solution:

Step 1:
I recently set up a PDF rendering engine on Heroku using the Python library pdfkit. There was a bit of extra work to get pdfkit working on Heroku.

Step 1: Install the wkhtmltopdf buildpack

https://github.com/dscout/wkhtmltopdf-buildpack

In vscode powershell, type:

heroku buildpacks:add https://github.com/dscout/wkhtmltopdf-buildpack.git

Then:

heroku config:set WKHTMLTOPDF_VERSION="0.12.4"

Then, Step 2:

Change your code:

config = pdfkit.configuration(wkhtmltopdf='./bin/wkhtmltopdf')

pdf = pdfkit.from_string(html, False, options=options, configuration=config)

My example:

config = pdfkit.configuration(wkhtmltopdf='./bin/wkhtmltopdf')
pdf = pdfkit.from_string(rendered,"output.pdf", configuration=config, css=css, options=kitoptions)
