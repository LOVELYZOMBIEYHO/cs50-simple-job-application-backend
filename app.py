from datetime import datetime, date, timedelta
import os
from flask import Flask, jsonify, render_template, session, request, redirect, send_file,make_response,Response,url_for
import flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import json
from flask_cors import CORS
from werkzeug.utils import send_file
from io import BytesIO
import csv
import pdfkit
from werkzeug.wrappers import response


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'sqlite.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = 'BAD_SECRET_KEY'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)



class Applicant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20),nullable=False)
    lastName = db.Column(db.String(20),nullable=False)
    idNo = db.Column(db.String(20), unique=True,nullable=False)
    applied_position = db.Column(db.String(20),nullable=False)
    expected_salary = db.Column(db.Float(10),nullable=False)
    date_availability = db.Column(db.Date, nullable=False)
    full_or_part_time = db.Column(db.String(20),nullable=False)
    sex = db.Column(db.String(10),nullable=False)
    address = db.Column(db.String(100),nullable=False)
    phone = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(40),nullable=False)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adminName = db.Column(db.String(25),nullable=False,unique=True)
    adminPassword = db.Column(db.String(30),nullable=False,unique=True)
 



@app.route('/', methods=["GET", "POST"])
def Home():

    return "Home"



@app.route('/jobapply', methods=["GET", "POST"])
def jobApply():
    if request.method =="POST":
        jobApplyData = request.json

        applicantAdd = Applicant(firstName=jobApplyData["firstName"], lastName=jobApplyData["lastName"], idNo=jobApplyData["idNo"], applied_position=jobApplyData["applied_position"], expected_salary=jobApplyData["expected_salary"], date_availability=datetime.strptime(jobApplyData["date_availability"],'%Y-%m-%d').date(), full_or_part_time=jobApplyData["full_or_part_time"], sex=jobApplyData["sex"], address=jobApplyData["address"], phone=jobApplyData["phone"], email=jobApplyData["email"])
        print(type(jobApplyData["date_availability"]))
        db.session.add(applicantAdd)
        db.session.commit()

        return jsonify(jobApplyData)

    else:
        return "GET"



@app.route('/login', methods=["GET", "POST"])
def login_admin():

    session.clear()
    if request.method =="POST":
        adminName = request.json["adminName"]
        adminPassword = request.json["adminPassword"]




        admin = Admin.query.filter_by(adminName=adminName).first()
        
    
        if admin is None:
            return jsonify({"error": "Unauthorized"}), 401
        elif adminPassword != admin.adminPassword:
            return jsonify({"error": "Incorrect Password"}), 401

        else:
            session["admin_id"] = admin.id
            return jsonify(id=admin.id)

        
            

    else:
        return "get"



# Check Login, 
@app.route('/admin', methods=["GET"])
def admin():
    if 'admin_id' in session:
        admin_id = session["admin_id"]
        return jsonify({
                "message": "You are admin now"
            })

    else:
        return jsonify({
                "message": "Please login"
            }),401
    return "get"

# Data View
@app.route('/data', methods=["GET", "POST"])
def data_view():

    if request.method =="POST":
        if 'admin_id' in session:
            admin_id = session["admin_id"]
            return jsonify({
                    "message": "You are admin now"
                })

        else:
            return redirect("/login")


@app.route("/download", methods=["GET", "POST"])
def download():
    if request.method == "POST":
        file_data = Applicant.query.all()

        
        with open('output.csv', 'w', newline='') as csvfile:
            # Use CSV writer module
            writer = csv.writer(csvfile)

            # Write first row (Header)
            writer.writerow(["Id", "FirstName", "LastName","ID no.","Applied Position","Expected Salary","Date Availability","Full or Part Time","Sex","Address","Phone","Email"])

            # Write all information from Sqlite db
            for i in file_data:
                writer.writerow([i.id, i.firstName, i.lastName, i.idNo,i.applied_position,i.expected_salary,i.date_availability,i.full_or_part_time,i.sex,i.address,i.phone,i.email])

        #  Simple Set cookieValue = 1, if there are several admins, it should use query to find db
        cookieValue = request.json["id"]
        if cookieValue == "1":
            return flask.send_file('output.csv', as_attachment=True) 
        else:
            return jsonify({"error": "Unauthorized"}), 401


    else:
        return "get"


@app.route("/pdf", methods=["GET", "POST"])
def all_applicants():
    allApplicantData = Applicant.query.all()
    applicantsList = []

    for allApplicant in allApplicantData:
        applicantsList.append({'id':allApplicant.id,'firstName':allApplicant.firstName,'lastName':allApplicant.lastName,'idNo':allApplicant.idNo,'applied_position':allApplicant.applied_position,'expected_salary':allApplicant.expected_salary,'date_availability':allApplicant.date_availability,'full_or_part_time':allApplicant.full_or_part_time,'sex':allApplicant.sex,'address':allApplicant.address,'phone':allApplicant.phone,'email':allApplicant.email})
    
    print(type(applicantsList))
    return jsonify(applicantsList)




@app.route("/pdf/<id>", methods=["GET", "POST"])
def pdf_template(id):

    pdfApplicantData = Applicant.query.filter_by(id=id).first()
    print(pdfApplicantData)
    rendered = render_template("pdf_template.html", id=id, firstName=pdfApplicantData.firstName, lastName= pdfApplicantData.lastName,idNo= pdfApplicantData.idNo,applied_position= pdfApplicantData.applied_position,expected_salary= pdfApplicantData.expected_salary,date_availability= pdfApplicantData.date_availability,full_or_part_time= pdfApplicantData.full_or_part_time,sex= pdfApplicantData.sex,address= pdfApplicantData.address,phone= pdfApplicantData.phone,email= pdfApplicantData.email)
    
    #  Make PDF and output

    css = ['templates/bootstrap.min.css']
    kitoptions = {"enable-local-file-access": None}
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    pdf = pdfkit.from_string(rendered,"output.pdf", configuration=config, css=css, options=kitoptions)
    return flask.send_file('output.pdf', as_attachment=True)
    




