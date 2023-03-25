from flask import Blueprint, render_template, request, redirect, session, flash
from . import db
from .models import Users, Roles, Donors, MedicalConditions, Donations, Appointment
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
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        user = Users.get_by_email(email)

        if user:
            print("User found:", user.Name, user.Email)
            if user.check_password(password):
                session['email'] = email
                print("Email added to session:", session['email'])

                if int(user.Role) == 1:
                    return redirect('/main')
                else:
                    print("Redirecting to staff page")
                    return redirect('/staff')

            else:
                flash('Invalid password', 'error')
        else:
            flash('Email does not exist', 'error')
        
        return render_template('login.html', error='Invalid email or password')
    else:
        return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    medical_conditions = MedicalConditions.query.all()
    print("Medical conditions:", medical_conditions)
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        dob = request.form['dob']
        gender = request.form['gender']
        phone = request.form['phone']
        weight = request.form['weight']
        password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        medical_history_id = request.form['medical_history']

        blood_type = request.form['blood_type']
        address = request.form['address']

        # Calculate age from date of birth
        age = calculate_age(dob)

        # Check whether email already exists
        user = Users.get_by_email(email)
        if user:
            flash('Email already exists', category='error')
            return render_template('register.html', medical_conditions=medical_conditions)

        # Create user and donor objects
        user = Users(Name=name, Email=email, Phone=phone, Password=password, Role=1)
        db.session.add(user)
        db.session.commit()

        donor = Donors(DonorName=name, DonorAge=age, DonorGender=gender, DonorWeight=weight, UserID=user.UserID, BloodType=blood_type, DonorAddress=address)

        # Add medical history to donor if selected
        if medical_history_id != 'None':
            medical_condition = MedicalConditions.query.filter_by(Name=medical_history_id).first()
            print("Medical condition:", medical_condition)
            if medical_condition:
                print("Medical condition ID:", medical_condition.MedicalConditionID)
                donor.DonorMedicalHistory = medical_condition.MedicalConditionID
            else:
                flash('Invalid medical condition selected', category='error')
                return render_template('register.html', medical_conditions=medical_conditions)

        # Update donor with user ID
        donor.UserID = user.UserID
        db.session.add(donor)
        db.session.commit()

        session['email'] = email
        return redirect('/login')
    else:
        return render_template('register.html', medical_conditions=medical_conditions)

@auth.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')