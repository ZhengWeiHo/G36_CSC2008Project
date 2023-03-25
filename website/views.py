from sqlalchemy import select, and_, join
from . import db
from .models import *
from flask import Blueprint, Flask, render_template, request, redirect, session, flash, jsonify
from .models import Users, Donors, Appointment, MedicalConditions, Slots
from datetime import datetime

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

@views.route('/filter-donation-history', methods=['GET'])
def filter_donation_history():
    logged_in_user_email = session['email']
    user = Users.get_by_email(logged_in_user_email)
    donor_id = user.donor.DonorID

    # Get filter parameters from the request
    filter_date = request.args.get('date')
    filter_quantity = request.args.get('quantity')
    filter_location = request.args.get('location')

    # Apply filters to the query based on the user's input
    query = Donations.query.filter(Donations.DonorID == donor_id)

    if filter_date:
        query = query.filter(Donations.DonationDate == filter_date)

    if filter_quantity:
        query = query.filter(Donations.Quantity == filter_quantity)

    if filter_location:
        query = query.filter(Donations.Location == filter_location)

    filtered_donations = query.all()

    response = [
        {
            "date": donation.DonationDate.strftime('%Y-%m-%d'),
            "quantity": donation.Quantity,
            "location": donation.Location
        }
        for donation in filtered_donations
    ]

    return jsonify(response)

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
    
    return render_template('appointment.html')

@views.route('/trackappointment')
def trackappointment():

    # Get logged in user's email
    logged_in_user_email = session['email']

    # Get user from Users table based on logged in user's email
    user = Users.get_by_email(logged_in_user_email)

    # Get DonorID for the logged-in user
    donor_id = user.donor.DonorID

    # Define a join query to fetch the required columns for the logged-in user with the DonationCenter name and Slot start/end time
    stmt = (db.session.query(Appointment.Date, Appointment.Status, DonationCenter.Name, Slots.StartTime, Slots.EndTime)
        .join(DonationCenter, DonationCenter.DonationCenterID == Appointment.DonationCenterID)
        .join(Slots, Slots.SlotID == Appointment.SlotID)
        .join(Donors, Donors.DonorID == Appointment.DonorID)
        .filter(Donors.DonorID == donor_id))

    result = stmt.all()

    return render_template('trackappointment.html', appointments=result)

@views.route('/available-slots', methods=['GET'])
def availableSlots():
    selected_date = request.args.get('date')
    donation_center_id = int(request.args.get('center_id'))

    # Subquery to count the number of appointments for the selected date
    subquery = (
        db.session.query(Appointment.SlotID, db.func.count(Appointment.AppointmentID).label('booked_count'))
        .filter(Appointment.Date == selected_date)
        .group_by(Appointment.SlotID)
        .subquery()
    )

    # Join the subquery with the Slots table to get the booked_count value
    available_slots = (
        db.session.query(Slots, subquery.c.booked_count)
        .outerjoin(subquery, Slots.SlotID == subquery.c.SlotID)
        .filter(Slots.DonationCenterID == donation_center_id)
        .group_by(Slots.SlotID)
        .having(db.func.coalesce(subquery.c.booked_count, 0) < Slots.Max_Bookings)
        .all()
    )

    response = [
        {
            "slot_id": slot.SlotID,
            "start_time": slot.StartTime.strftime('%H:%M'),
            "end_time": slot.EndTime.strftime('%H:%M'),
            "booked_count": booked_count if booked_count is not None else 0,
            "max_bookings": slot.Max_Bookings,
        }
        for slot, booked_count in available_slots
    ]

    return jsonify(response)

@views.route('/appointment-submit', methods=['POST'])
def appointmentSubmit():
    center_id = request.form['center']
    appointment_date = request.form['date']
    # Parse the string into a date object
    appointment_date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
    
    # Get the logged-in user's email from the session
    logged_in_user_email = session['email']

    # Get user from Users table based on logged in user's email
    user = Users.get_by_email(logged_in_user_email)

    # Get DonorID for the logged-in user
    donor_id = user.donor.DonorID

    slot_id = request.form['time']

    # Create the Appointment object with the parsed date object
    appointment = Appointment(Date=appointment_date, Status="Upcoming", DonorID=donor_id, DonationCenterID=center_id, SlotID=slot_id)
    db.session.add(appointment)
    db.session.commit()

    # Update the Booked_Count for the selected slot
    slot = Slots.query.get(slot_id)
    slot.Booked_Count += 1
    db.session.commit()

    return "Appointment created successfully!"

# ----------------------------
# For staff page
# ----------------------------
@views.route('/donationshist')
def donations():
    donations = db.session.query(Donations, Donors, Users)\
        .join(Donors, Donations.DonorID == Donors.DonorID)\
        .join(Users, Donors.UserID == Users.UserID)\
        .all()
    return render_template('allhistory.html', donations=donations)


@views.route('/changestatus')
def changestatus():
    appointments = Appointment.query.all()
    return render_template('status.html', appointments=appointments)

@views.route('/appointments/<int:id>/update', methods=['POST'])
def update_appointment(id):
    # Get the appointment to update
    appointment = Appointment.query.filter_by(AppointmentID=id).first()

    
    appointment.Status = request.form['status']
   

    # Add the updated appointment to the session and commit the transaction
    db.session.add(appointment)
    db.session.commit()

    return redirect('/changestatus')