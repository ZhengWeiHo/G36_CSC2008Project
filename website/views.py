#from flask import Blueprint
from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)
app.secret_key = "secret_key"

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'blood_donation'

mysql = MySQL(app)

@app.route('/')
def home():
     return render_template('base.html')

# @app.route('/')
# def home():
#     if 'username' in session:
#         return render_template('base.html', username=session['username'])
#     else:
#         return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        username = request.form['username']
        password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, phone, username, password) VALUES (%s, %s, %s, %s, %s)", (name, email, phone, username, password))
        mysql.connection.commit()
        cur.close()

        session['username'] = username
        return redirect('/')
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s", [username])
        user = cur.fetchone()
        cur.close()

        if user:
            if bcrypt.checkpw(password, user[4].encode('utf-8')):
                session['username'] = username
                return redirect('/')
            else:
                return render_template('login.html', error='Invalid username or password')
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
