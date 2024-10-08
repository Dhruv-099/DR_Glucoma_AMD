from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Doctor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    patients = db.relationship('Patient', backref='doctor', lazy=True)  
    

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    age = db.Column(db.Integer())
    gender = db.Column(db.String(1))
    phone_number = db.Column(db.String(20))  
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))  
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    photo=db.Column(db.String(600))

class Patient_history(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    patient_id=db.Column(db.String,db.ForeignKey('patient.id'))
    name= db.Column(db.String(150))
    description= db.Column(db.String(150))
    date=db.Column(db.DateTime(timezone=True),default=func.now)
    photo=db.Column(db.String(600))
    patient=db.relationship('Patient',backref='history')
