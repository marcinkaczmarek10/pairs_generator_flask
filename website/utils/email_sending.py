from flask_mail import Mail, Message
from flask import url_for
from threading import Thread
from flask import current_app

mail = Mail()


class MailError(Exception):
    pass


def email_message(subject: str, recipients: list, body: str):
    message = Message(
        subject=subject,
        recipients=recipients,
        body=body
    )
    return message


def send_mail(app, message):
    with app.app_context():
        mail.send(message)


def send_email(message):
    app = current_app._get_current_object()
    thr = Thread(target=send_mail, args=[app, message])
    thr.start()
    return thr


def send_reset_password_mail(user):
    token = user.get_token()
    message = email_message(
        'Password reset for Random Pairs Generator',
        [user.email],
        f"""Click the link below to reset your password.
        {url_for(
            'auth.reset_password',
            token=token,
            _external=True
        )}"""
    )
    send_email(message)


def send_verification_mail(user):
    token = user.get_token()
    message = email_message(
        'Email confirmation for Random Pairs Generator',
        [user.email],
        f"""Click the link below to confirm your email.
            {url_for(
            'auth.confirm_email',
            token=token,
            _external=True
        )}
    """
    )
    send_email(message)


def send_mail_to_pairs(recipients, title, body):
    for recipient in recipients:
        message = email_message(
            title,
            [recipient['first_person_email']],
            f'Hey {recipient["first_person_name"]}! You picked: {recipient["second_person_name"]}!\n{body}')
        send_email(message)
