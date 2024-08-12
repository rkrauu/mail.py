import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

# Function to send email with attachment
def send_email(sender_email, receiver_email, subject, message, smtp_server, smtp_port, login, password, attachment=None):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        # Attach the file
        if attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {attachment.name}")
            msg.attach(part)

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(login, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()

        return "Email sent successfully!"
    except Exception as e:
        return str(e)

# Streamlit app
st.title('Email Sender App with Attachment')

st.sidebar.header('Email Configuration')
smtp_server = st.sidebar.text_input('SMTP Server', 'smtp.gmail.com')
smtp_port = st.sidebar.number_input('SMTP Port', 587)
login = st.sidebar.text_input('Login Email')
password = st.sidebar.text_input('Password', type='password')

st.header('Compose Email')
sender_email = st.text_input('Sender Email', login)
receiver_email = st.text_input('Receiver Email')
subject = st.text_input('Subject')
message = st.text_area('Message')
attachment = st.file_uploader("Choose a file", type=["txt", "pdf", "png", "jpg", "jpeg", "gif", "docx", "xlsx"])

if st.button('Send Email'):
    result = send_email(sender_email, receiver_email, subject, message, smtp_server, smtp_port, login, password, attachment)
    st.write(result)
