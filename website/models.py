from . import db
from flask_sqlalchemy import SQLAlchemy
import bcrypt

# db = SQLAlchemy()

class Users(db.Model):
    UserID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False, unique=True)
    Phone = db.Column(db.String(50), nullable=False)
    Password = db.Column(db.String(75), nullable=False)
    Role = db.Column(db.Integer, db.ForeignKey('roles.RoleID'), nullable=False)

    role_relation = db.relationship('Roles')
    donor = db.relationship('Donors', backref='user', uselist=False)

    # def create(self):
    #     db.session.add(self)
    #     db.session.commit()

    # @staticmethod
    def get_by_email(email):
        return Users.query.filter_by(Email=email).first()

    def check_password(self, password):
        return bcrypt.checkpw(password, self.Password)
    
class Roles(db.Model):
    RoleID = db.Column(db.Integer, primary_key=True)
    RoleName = db.Column(db.String(10), unique=True)

    users = db.relationship('Users')
    staff = db.relationship('Staff', backref='role')

class MedicalConditions(db.Model):
    MedicalConditionID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(75), unique=True)

    donors = db.relationship('Donors', backref='medical_condition')

class Donors(db.Model):
    DonorID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'))
    DonorName = db.Column(db.String(50))
    DonorAge = db.Column(db.Integer)
    DonorGender = db.Column(db.String(1))
    DonorWeight = db.Column(db.Float)
    BloodType = db.Column(db.String(3))
    DonorAddress = db.Column(db.String(250))
    DonorMedicalHistory = db.Column(db.Integer, db.ForeignKey('medical_conditions.MedicalConditionID'), nullable=True)

    appointments = db.relationship('Appointment', backref='donor')
    donations = db.relationship('Donations', backref='donor')

class Donations(db.Model):
    DonationID = db.Column(db.Integer, primary_key=True)
    DonorID = db.Column(db.Integer, db.ForeignKey('donors.DonorID'))
    DonationDate = db.Column(db.Date, nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    Location = db.Column(db.String(50), nullable=False)

class Appointment(db.Model):
    AppointmentID = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.DateTime, nullable=False)
    DonorID = db.Column(db.Integer, db.ForeignKey('donors.DonorID'))
    DonationCenterID = db.Column(db.Integer, db.ForeignKey('donation_center.DonationCenterID'))
    SlotID = db.Column(db.Integer, db.ForeignKey('slots.SlotID'))

class DonationCenter(db.Model):
    DonationCenterID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Address = db.Column(db.String(100), nullable=False)

    appointments = db.relationship('Appointment', backref='donation_center')
    slots = db.relationship('Slots', backref='donation_center')

class Slots(db.Model):
    SlotID = db.Column(db.Integer, primary_key=True)
    StartTime = db.Column(db.Time, nullable=False)
    EndTime = db.Column(db.Time, nullable=False)
    Max_Bookings = db.Column(db.Integer, nullable=False)
    Booked_Count = db.Column(db.Integer, nullable=False)
    DonationCenterID = db.Column(db.Integer, db.ForeignKey('donation_center.DonationCenterID'))

    appointments = db.relationship('Appointment', backref='slot')

class Staff(db.Model):
    StaffID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False, unique=True)
    Password = db.Column(db.String(75), nullable=False)
    Role = db.Column(db.String(10), db.ForeignKey('roles.RoleID'))