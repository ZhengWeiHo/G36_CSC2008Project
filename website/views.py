#Not Completed, got Errors

from . import db
from .models import *
from flask import Blueprint, Flask, render_template, request, redirect, session, flash
from sqlalchemy import select
from .models import Appointment

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('index.html')

@views.route('/main')
def mainpage():
    return render_template('main.html')

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


@views.route('/appointment', methods=['POST'])
def appointment():
    appointment_id = request.form['appointment_id']
    appointment_date = request.form['date']
    donor_id = request.form['donor_id']
    center_id = request.form['center_id']
    slot_id = request.form['slot_id']

     # Insert the data into the Appointment table
    appointment = Appointment(ApointmentID=appointment_id, Date=appointment_date, DonorID=donor_id, DonationCenterID=center_id, SlotID=slot_id)
    db.session.add(appointment)
    db.session.commit()
    
    return "Appointment created successfully!"