#!/usr/bin/python

from flask_mail import Message
from app import app, mail
from config import ADMINS

sender = 'noah@beyondmapping.com'
receivers = ['wtgeographer@gmail.com']

message = """From: From Person <from@fromdomain.com>
To: To Person <to@todomain.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

# email server
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# administrator list
ADMINS = ['your-gmail-username@gmail.com']

msg = Message('test subject', sender=ADMINS[0], recipients=ADMINS)
msg.body = 'text body'
msg.html = '<b>HTML</b> body'
with app.app_context():
...     mail.send(msg)
....