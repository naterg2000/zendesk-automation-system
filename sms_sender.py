# going to use this to send text messages to each Google Voice 
# number to avoid losing the numbers and accounts

import smtplib
from email.mime.text import MIMEText
import sys
 
CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com"
}

credentials_file = open('gmail_password.txt', 'r')
credentials = credentials_file.readline().split(',')

EMAIL = credentials[0]
PASSWORD = credentials[1]

def get_recipient(phone_number, carrier):
    return phone_number + CARRIERS[carrier]

def compile_message(phone_number, carrier, message):

    recipient = get_recipient(phone_number, carrier)
    msg = MIMEText(message, 'plain')
    msg['To'] = recipient
    message = 'here is the email'
    msg.attach(MIMEText(message))

    return msg


def send_message(message):

    msg = compile_message('18184728763', 'att', 'hi')

    mail=smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.ehlo()
    mail.login(EMAIL, PASSWORD)

    mail.sendmail(EMAIL, get_recipient('18184728763', 'att'), msg)

    mail.quit()
 
send_message('hi')