#Not Completed, got Errors

from . import db
from .models import *
from flask import Blueprint, Flask, render_template, request, redirect, session, flash
from sqlalchemy import select

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('index.html')

@views.route('/main')
def mainpage():
    return render_template('main.html')

@views.route('/appointment')
def appointment():
    return render_template('appointment.html')

@views.route('/startcheck')
def startcheck():
    return render_template('startcheck.html')

@views.route('/donationhistory')
def donationhistory():
     # Define a query to fetch only the required columns
    stmt = select(Donations.DonationDate, Donations.Quantity, Donations.Location)
    
    # Execute the query
    result = db.session.execute(stmt)
    
    # Fetch all records as a list of namedtuples
    donations = result.fetchall()

    # Pass the donations data to the donationhistory.html template
    return render_template('donationhistory.html', donations=donations)