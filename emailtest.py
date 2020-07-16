import smtplib
from config import ema, emp

EMAIL_ADDRESS = ema
EMAIL_PASSWORD = emp

# https://www.youtube.com/watch?v=JRCJ6RtE3xU
with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    # Log into mail server
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    subject = 'Arrival Alert!'
    body = 'Someone has arrived at home!'

    msg = f'Subject: {subject}\n\n{body}'

    # Sender, receiver, message as parameters
    # Just send to myself for now
    smtp.sendmail(EMAIL_ADDRESS, 'tmiles7@vols.utk.edu', msg)