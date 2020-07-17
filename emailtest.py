import smtplib
from config import ema, emp, email_list

EMAIL_ADDRESS = ema
EMAIL_PASSWORD = emp

def em_send(name):

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
            # Just send to myself for now
            smtp.sendmail(EMAIL_ADDRESS, recipient, msg)