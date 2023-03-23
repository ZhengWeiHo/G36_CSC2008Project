from flask import Blueprint, render_template, request, redirect, session, flash
from . import db
from .models import Users, Roles, Donors
import bcrypt
import uuid

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        user = Users.get_by_email(email)
        

        if user and user.check_password(password):
            session['email'] = email

            # Show a notification of successful login
            flash('Login successful', 'success')
            return redirect('/main')
        else:
            return render_template('login.html', error='Invalid email or password')
    else:
        return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        user_role = 1

        # Check whether email already exists
        userEmail = Users.get_by_email(email)
        if userEmail:
            flash('Email already exists', category='error')
            return render_template('register.html')

        user = Users(Name=name, Email=email, Phone=phone, Password=password, Role=user_role.RoleID)
        db.session.add(user)
        db.session.commit()

        session['email'] = email
        return redirect('/login')
    else:
        return render_template('register.html')

@auth.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')