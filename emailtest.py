import smtplib
from config import email_address, email_password, email_list

EMAIL_ADDRESS = email_address
EMAIL_PASSWORD = email_password

def em_send(name):

    # Send notification to each person as specified in config
    for recipient in email_list:

    # https://www.youtube.com/watch?v=JRCJ6RtE3xU
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            # Log into mail server
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            subject = 'Arrival Alert!'

            # figured I'd try out fstring instead of .format
            body = f'{name} has arrived at home!'

            msg = f'Subject: {subject}\n\n{body}'

            # Sender, receiver, message as parameters
            smtp.sendmail(EMAIL_ADDRESS, recipient, msg)