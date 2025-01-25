import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_confirmation_email(receiver_address, name):
    mail_content = f'''
    Hola {name} has sido registrado/a como paciente en pacients_api by Gaston Gaitan con exito.
    '''

    sender_address = 'ggaitan1998@gmail.com'
    sender_pass = 'indq nvqe zskf ehgg'

    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Registro exitoso en pacients_api by Gaston Gaitan'   

    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')