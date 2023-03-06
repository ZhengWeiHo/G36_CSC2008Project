#Not Completed, got Errors

from flask import Flask, render_template, request, redirect, session
from models import db, User
import bcrypt

app = Flask(__name__)
app.secret_key = "secret_key"

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blood_donation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        role = 'user'

        user = User(Name=name, Email=email, Phone=phone, Password=password, Role=role)
        user.create()

        session['email'] = email
        return redirect('/')
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        user = User.get_by_email(email)

        if user and user.check_password(password):
            session['email'] = email
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid email or password')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

