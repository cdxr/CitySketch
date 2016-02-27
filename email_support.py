# functions containing email support

from flask.ext.mail import Mail, Message
from index import app

mail = Mail(app)

def send_email(subject, sender, recipients, text_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    mail.send(msg)
    return True
