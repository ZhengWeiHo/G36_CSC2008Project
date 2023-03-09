from . import db
from flask_sqlalchemy import SQLAlchemy
import bcrypt

# db = SQLAlchemy()

class Users(db.Model):
    UserID = db.Column(db.String(36), primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False, unique=True)
    Phone = db.Column(db.String(50), nullable=False)
    Password = db.Column(db.String(75), nullable=False)
    Role = db.Column(db.String(10), nullable=False)

    

    # def create(self):
    #     db.session.add(self)
    #     db.session.commit()

    # @staticmethod
    def get_by_email(email):
        return Users.query.filter_by(Email=email).first()

    def check_password(self, password):
        return bcrypt.checkpw(password, self.Password)


