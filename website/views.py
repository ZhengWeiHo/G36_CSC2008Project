from sqlalchemy import select
from . import db
from .models import *
from flask import Blueprint, Flask, render_template, request, redirect, session, flash
from .models import Appointment

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('index.html')

def is_logged_in():
    return 'email' in session

@views.route('/main')
def mainpage():
    if is_logged_in():
        return render_template('main.html')
    else:
        flash('Please log in to access this page.', 'error')
        return redirect('/login')
    
@views.route('/staff')
def staffpage():
    if is_logged_in():
        return render_template('staff.html')
    else:
        flash('Please log in to access this page.', 'error')
        return redirect('/login')

@views.route('/startcheck')
def startcheck():
    return render_template('startcheck.html')

@views.route('/updatestatus')
def updatestatus():
    return redirect('/changestatus')

@views.route('/alldonationhistory')
def allhistory():
    return redirect('/donationshist')

# @views.route('/eligibility')
# def eligibility():
#     email = session.get('email')
#     if email:
#         user = Users.query.filter_by(Email=email).first()
#         donor = user.donor
#         user_medical_condition = donor.medical_condition
#         return render_template('eligibility.html', user_medical_condition=user_medical_condition)
#     else:
#         return redirect('/login')

@views.route('/donationhistory')
def donationhistory():
    # Get logged in user's email
    logged_in_user_email = session['email']

    # Get user from Users table based on logged in user's email
    user = Users.get_by_email(logged_in_user_email)

    # Get DonorID for the logged-in user
    donor_id = user.donor.DonorID

    # Define a query to fetch only the required columns for the logged-in user
    stmt = select(Donations.DonationDate, Donations.Quantity, Donations.Location).where(Donations.DonorID == donor_id)

    # Execute the query
    result = db.session.execute(stmt)

    # Fetch all records as a list of namedtuples
    donations = result.fetchall()

    # Pass the donations data to the donationhistory.html template
    return render_template('donationhistory.html', donations=donations)


@views.route('appointment')
def appointment():
    return render_template('appointment.html')


@views.route('/appointment-submit', methods=['POST'])
def appointmentSubmit():
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