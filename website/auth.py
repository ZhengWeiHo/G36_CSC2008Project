from flask import Blueprint, render_template, request, redirect, session, flash
from . import db
from .models import Users, Roles, Donors, MedicalConditions
import bcrypt
import datetime

auth = Blueprint('auth', __name__)

def calculate_age(date_of_birth):
    birthdate = datetime.datetime.strptime(date_of_birth, '%Y-%m-%d')
    today = datetime.date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:
        print("Email already in session:", session['email'])
        return redirect('/main')

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        user = Users.get_by_email(email)

        if user:
            print("User found:", user.Name, user.Email)
            if user.check_password(password):
                session['email'] = email
                print("Email added to session:", session['email'])

                # Show a notification of successful login
                flash('Login successful', 'success')
                return redirect('/main')
            else:
                flash('Invalid password', 'error')
        else:
            flash('Email does not exist', 'error')
        
        return render_template('login.html', error='Invalid email or password')
    else:
        return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        dob = request.form['dob']
        phone = request.form['phone']
        weight = request.form['weight']
        password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        medical_history_id = request.form['medical_history']

        # Calculate age from date of birth
        birthdate = datetime.datetime.strptime(dob, '%Y-%m-%d')
        today = datetime.date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

        # Check whether email already exists
        user = Users.get_by_email(email)
        if user:
            flash('Email already exists', category='error')
            return render_template('register.html')

        # Create user and donor objects
        user = Users(Name=name, Email=email, Phone=phone, Password=password, Role=1)
        donor = Donors(DonorName=name, DonorAge=age, DonorWeight=weight, UserID=user.UserID, BloodType=None)

        # Add medical history to donor if selected
        if medical_history_id != 'None':
            medical_condition = MedicalConditions.query.filter_by(MedicalConditionID=medical_history_id).first()
            donor.DonorMedicalHistory = medical_condition.MedicalConditionID

        db.session.add(user)
        db.session.add(donor)
        db.session.commit()

        session['email'] = email
        return redirect('/login')
    else:
        return render_template('register.html')

@auth.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')