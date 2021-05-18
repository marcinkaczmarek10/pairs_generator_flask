from flask_mail import Mail, Message
from flask import url_for

mail = Mail()


def email_message(subject: str, sender: str, recipients: list, body: str):
    message = Message(
        subject=subject,
        sender=sender,
        recipients=recipients,
        body=body
    )
    return message


def send_reset_password_mail(user):
    token = user.get_token()
    message = email_message(
        'Password reset for Random Password Generator',
        'noreply@exaple.com',
        [user.email],
        f"""Click the link below to reset your password.
        {url_for(
            'auth.reset_password',
            token=token,
            _external=True
        )}
"""
    )
    mail.send(message)
