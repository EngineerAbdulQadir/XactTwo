import streamlit as st
import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
from datetime import datetime

# --- Set Page Configuration Early ---
st.set_page_config(page_title="Xact Two - Booking Agent", page_icon="🚀", layout="wide")

# --- Load Environment Variables ---
load_dotenv()
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

# --- Inject Custom CSS ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        /* Updated Color Scheme */
        :root {
            --primary-blue: #2A4E6C;
            --accent-blue: #3B8ED0;
            --light-blue: #E6F4F1;
            --dark-blue: #1A364D;
            --text-primary: #2D3436;
        }
        /* Overall app background */
        .stApp {
            background: #f8f9fa !important;
        }
                
        /* Container for the booking form */
        .booking-container {
            max-width: 700px;
            margin: 50px auto;
            background: #fffff;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        }
        /* Header styling */
        .booking-header {
            text-align: center;
            margin-bottom: 30px;
        }
        .booking-header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #2575fc, #6a11cb);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            font-weight: 700;
        }
        .booking-header p {
            font-size: 1.1rem;
            color: #555;
        }
        /* Form elements styling */
        .stTextInput>div>div>input,
        .stTextArea>div>div>textarea,
        .stDateInput>div>div>input,
        .stTimeInput>div>div>input {
            font-family: 'Poppins', sans-serif !important;
            font-size: 1rem;
        }
        /* Footer styling */
        .custom-footer {
            text-align: center;
            margin-top: 40px;
            font-size: 0.9rem;
            color: #777;
        }
    </style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown("""
    <div class="booking-header">
        <h1>🚀 Xact Two</h1>
        <p>Book an appointment with Xactrix AI officials to discuss how our advanced AI solutions can transform your business.</p>
    </div>
""", unsafe_allow_html=True)

# --- Booking Form Section ---
with st.form("booking_form"):
    name = st.text_input("Your Name", max_chars=100)
    email = st.text_input("Your Email", max_chars=100)
    phone = st.text_input("Your Phone Number", max_chars=15)
    appointment_date = st.date_input("Preferred Appointment Date")
    appointment_time = st.time_input("Preferred Appointment Time")
    message = st.text_area("Additional Information / Message", height=150)
    
    submit = st.form_submit_button("Book Appointment")

if submit:
    if not name or not email:
        st.error("Please provide at least your name and email address.")
    else:
        # Format appointment date and time
        appt_date_str = appointment_date.strftime('%B %d, %Y')
        appt_time_str = appointment_time.strftime('%I:%M %p')
        
        # Email content for the user (confirmation)
        user_subject = "Appointment Confirmation - Xactrix AI"
        user_body = f"""Dear {name},

Thank you for booking an appointment with Xactrix AI.
Here are your appointment details:

Date: {appt_date_str}
Time: {appt_time_str}
Phone: {phone if phone else 'Not Provided'}
Message: {message if message else 'N/A'}

Our team will contact you shortly.

Best regards,
Xactrix AI
"""
        # Email content for the company official (notification)
        official_subject = "New Appointment Booking - Xactrix AI"
        official_body = f"""A new appointment has been booked:

Name: {name}
Email: {email}
Phone: {phone if phone else 'Not Provided'}
Date: {appt_date_str}
Time: {appt_time_str}
Message: {message if message else 'N/A'}

Please follow up with the client at your earliest convenience.
"""
        # Attempt to send emails via SMTP
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(SMTP_EMAIL, SMTP_PASSWORD)
                
                # Prepare and send confirmation email to the user
                user_msg = EmailMessage()
                user_msg['Subject'] = user_subject
                user_msg['From'] = SMTP_EMAIL
                user_msg['To'] = email
                user_msg.set_content(user_body)
                
                # Prepare and send notification email to the company official
                official_msg = EmailMessage()
                official_msg['Subject'] = official_subject
                official_msg['From'] = SMTP_EMAIL
                official_msg['To'] = SMTP_EMAIL
                official_msg.set_content(official_body)
                
                smtp.send_message(user_msg)
                smtp.send_message(official_msg)
                
            st.success("Your appointment has been booked successfully! A confirmation email has been sent to you.")
        except Exception as e:
            st.error(f"Error sending email: {str(e)}")

st.markdown("</div>", unsafe_allow_html=True)

# --- Footer Section ---
st.markdown("""
    <div class="custom-footer">
        <hr>
        <p>Made with ❤️ by Engineer Abdul Qadir <br>
        Version 0.1 | Xactrix AI Engine</p>
    </div>
""", unsafe_allow_html=True)
