from flask_mail import Mail, Message
from flask import url_for
from threading import Thread
from flask import current_app, render_template

mail = Mail()


class MailError(Exception):
    pass


def email_message(subject: str, recipients: list, template: str, context: dict):
    body_html = render_template(template, **context)
    message = Message(
        subject=subject,
        recipients=recipients
    )
    message.html = body_html
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
        'email/password_reset_email.html',
        {'token': url_for(
            'auth.reset_password',
            token=token,
            _external=True
        )}
    )
    send_email(message)


def send_verification_mail(user):
    token = user.get_token()
    message = email_message(
        'Email confirmation for Random Pairs Generator',
        [user.email],
        'email/verification_email.html',
        {'token': url_for(
            'auth.confirm_email',
            token=token,
            _external=True
        )}
    )
    send_email(message)


def send_mail_to_pairs(recipients, title, body):
    for recipient in recipients:
        message = email_message(
            title,
            [recipient['first_person_email']],
            'email/pairs_email.html',
            {'first_person_name': recipient['first_person_name'],
             'second_person_name': recipient["second_person_name"]}
        )
        send_email(message)
