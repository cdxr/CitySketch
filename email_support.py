# functions containing email support

from flask_mail import Mail, Message


def send_email(app, subject, sender, recipients, text_body):
    mail = Mail(app)
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    mail.send(msg)
    return True
