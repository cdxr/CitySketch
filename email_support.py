from flask import Flask
from flask_mail import Mail, Message
from index import app
import setup

app.config['MAIL_SERVER'] = setup.MAIL_SERVER
app.config['MAIL_PORT'] = setup.MAIL_PORT
app.config['MAIL_USERNAME'] = setup.MAIL_USERNAME
app.config['MAIL_PASSWORD']= setup.MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = setup.MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = setup.MAIL_USE_SSL

mail = Mail(app)

def send_email(subject, sender, recipients, text_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    mail.send(msg)
    return True
