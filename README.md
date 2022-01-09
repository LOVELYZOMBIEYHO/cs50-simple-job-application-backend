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

Python version 3.10.0
