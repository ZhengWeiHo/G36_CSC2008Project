import csv
import random
from datetime import datetime, timedelta
import os
import bcrypt
import base64

# Generate a random date between two dates
def random_date(start, end):
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

# Set date range for generating donation dates
start_date = datetime(2020, 1, 1)
end_date = datetime(2023, 3, 25)

# Set parameters for generating users
user_count = 10
phone_prefix = "+65"
user_password = "password"

# Set parameters for generating donors
donor_medical_conditions = list(range(1, 9))
donor_address = "Singapore"

# Set parameters for generating donations
donor_ids = list(range(1, user_count + 1))
locations = ['BloodBank@Outram', 'BloodBank@DhobyGhaut', 'BloodBank@Woodlands', 'BloodBank@WestgateTower']

# Set output directory to the directory containing the script
output_dir = os.path.dirname(os.path.abspath(__file__))

# Open CSV files for writing
# Open CSV files for writing
users_file = open(os.path.join(output_dir, 'users.csv'), 'w', newline='')
donors_file = open(os.path.join(output_dir, 'donors.csv'), 'w', newline='')

users_fieldnames = ['UserID', 'Name', 'Email', 'Phone', 'Password', 'Role']
users_writer = csv.DictWriter(users_file, fieldnames=users_fieldnames)
users_writer.writeheader()

donors_fieldnames = ['DonorID', 'UserID', 'DonorName', 'DonorAge', 'DonorGender', 'DonorWeight', 'BloodType', 'DonorAddress', 'DonorMedicalHistory']
donors_writer = csv.DictWriter(donors_file, fieldnames=donors_fieldnames)
donors_writer.writeheader()

# Generate and write user and donor records
for i in range(1, user_count + 1):
    name = f"user{i}"
    email = f"{name}@example.com"
    phone = f"{phone_prefix}{random.randint(10000000, 99999999)}"
    password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())

    # Encode password before inserting to the database
    password = password.decode('utf-8')
    role = 1

    # Write user record to CSV
    user = {
        'UserID': i,
        'Name': name,
        'Email': email,
        'Phone': phone,
        'Password': password,
        'Role': role
    }
    users_writer.writerow(user)

    # Write donor record to CSV
    dob = random_date(start_date - timedelta(days=365 * 80), end_date - timedelta(days=365 * 16)).strftime('%Y-%m-%d')
    age = datetime.now().year - datetime.strptime(dob, '%Y-%m-%d').year
    donor_name = name
    donor_age = age
    donor_gender = random.choice(['M', 'F'])
    donor_weight = random.uniform(50, 100)
    blood_type = random.choice(['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'])
    donor_medical_history = random.choice([None] + donor_medical_conditions)

    donor = {
        'DonorID': i,
        'UserID': i,
        'DonorName': donor_name,
        'DonorAge': donor_age,
        'DonorGender': donor_gender,
        'DonorWeight': donor_weight,
        'BloodType': blood_type,
        'DonorAddress': donor_address,
        'DonorMedicalHistory': donor_medical_history
    }
    donors_writer.writerow(donor)

# Close CSV files
users_file.close()
donors_file.close()

print(f"{user_count} user records and donor records written to users.csv and donors.csv")

with open(os.path.join(output_dir, 'donations.csv'), 'w', newline='') as csvfile:
    fieldnames = ['DonationID', 'DonorID', 'DonationDate', 'Quantity', 'Location']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Generate and write 1,000 donation records
    for i in range(1, 1001):
        donation = {
            'DonationID': i,
            'DonorID': random.choice(donor_ids),
            'DonationDate': random_date(start_date, end_date).strftime('%Y-%m-%d'),
            'Quantity': random.randint(1, 5),
            'Location': random.choice(locations)
        }
        writer.writerow(donation)

print("1,000 donation records written to donations.csv in same directory as script")

appointments_file = open(os.path.join(output_dir, 'appointments.csv'), 'w', newline='')

appointments_fieldnames = ['AppointmentID', 'Date', 'Status', 'DonorID', 'DonationCenterID', 'SlotID']
appointments_writer = csv.DictWriter(appointments_file, fieldnames=appointments_fieldnames)
appointments_writer.writeheader()

appointment_count = 1000
statuses = ['Completed', 'Pending']
slot_ids = list(range(1, 33))
donation_center_ids = list(range(1, 5))

for i in range(1, appointment_count + 1):
    appointment_date = random_date(start_date, end_date).strftime('%Y-%m-%d')
    status = random.choice(statuses)
    donor_id = random.choice(donor_ids)
    donation_center_id = random.choice(donation_center_ids)
    slot_id = random.choice(slot_ids)

    appointment = {
        'AppointmentID': i,
        'Date': appointment_date,
        'Status': status,
        'DonorID': donor_id,
        'DonationCenterID': donation_center_id,
        'SlotID': slot_id
    }
    appointments_writer.writerow(appointment)

appointments_file.close()
print(f"{appointment_count} appointment records written to appointments.csv")