import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

def send_confirmation_email(new_patient, db):
    mail_content = f'''
    Hola {new_patient.name} has sido registrado/a como patiente en patients_api by Gaston Gaitan con exito.
    '''
    receiver_address = new_patient.email
    sender_address = os.environ.get('EMAIL_ADDRESS')
    sender_pass = os.environ.get('APP_PASSWORD')

    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = new_patient.email
    message['Subject'] = 'Registro exitoso en patients_api by Gaston Gaitan'   

    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()

    try:
        session.sendmail(sender_address, receiver_address, text)
        # Update the email_verification_sent field in the database
        patient = db.query(type(new_patient)).filter_by(email=receiver_address).first()
        if patient:
            patient.email_verification_sent = True
            db.commit()
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        session.quit()
    
    print('Mail Sent to ' + receiver_address)