from sqlalchemy import select
from . import db
from .models import *
from flask import Blueprint, Flask, render_template, request, redirect, session, flash
from .models import Users, Donors, Appointment, MedicalConditions, Slots

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

@views.route('/eligibility')
def eligibility():
    logged_in_user_email = session['email']
    user = Users.get_by_email(logged_in_user_email)
    donor = user.donor
    user_medical_condition = donor.medical_condition
    return render_template('eligibility_check.html', user_medical_condition=user_medical_condition)

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


@views.route('/appointment')
def appointment():
    slots = Slots.query.all()
    return render_template('appointment.html', slots=slots)



@views.route('/appointment-submit', methods=['POST'])
def appointmentSubmit():
    # Get the form data
    center_id = request.form['center']
    appointment_date = request.form['date'] + ' ' + request.form['time']
    donor_id = 1 # change this to the actual donor ID
    slot_id = 1 # change this to the actual slot ID

    # Insert the data into the Appointment table
    appointment = Appointment(Date=appointment_date, Status="Upcoming", DonorID=donor_id, DonationCenterID=center_id, SlotID=slot_id)
    db.session.add(appointment)
    db.session.commit()

    return "Appointment created successfully!"