#Not Completed, got Errors

import uuid
from . import db
from .models import Users
from flask import Blueprint, Flask, render_template, request, redirect, session, flash
import bcrypt

views = Blueprint('views', __name__)

# app = Flask(__name__)
# app.secret_key = "secret_key"

# # Database configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blood_donation.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db.init_app(app)

@views.route('/')
def home():
    return render_template('index.html')

# @views.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         phone = request.form['phone']
#         password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
#         role = 'user'
#         userid = str(uuid.uuid4())

#         user = Users(UserID=userid,Name=name, Email=email, Phone=phone, Password=password, Role=role)
#         db.session.add(user)
#         db.session.commit()

#         session['email'] = email
#         return redirect('/')
#     else:
#         return render_template('register.html')

# @views.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password'].encode('utf-8')

#         user = Users.get_by_email(email)
        

#         if user and user.check_password(password):
#             session['email'] = email

#             # Show a notification of successful login
#             flash('Login successful', 'success')
#             return render_template('main.html')
#         else:
#             return render_template('login.html', error='Invalid email or password')
#     else:
#         return render_template('login.html')

# @views.route('/logout')
# def logout():
#     session.pop('email', None)
#     return redirect('/')

@views.route('/main')
def mainpage():
    return render_template('main.html')

@views.route('/appointment')
def appointment():
    return render_template('appointment.html')

@views.route('/donationhistory')
def donationhistory():
    return render_template('donationhistory.html')