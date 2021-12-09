from flask_mail import Mail, Message
from flask import url_for
from threading import Thread
from flask import current_app

mail = Mail()


class MailError(Exception):
    pass


class SendMail:
    @staticmethod
    def _get_token(user):
        token = user.get_token()
        return token

    @staticmethod
    def email_message(subject: str, sender: str, recipients: list, body: str):
        message = Message(
            subject=subject,
            sender=sender,
            recipients=recipients,
            body=body
        )
        return message

    @staticmethod
    def send_mail(message):
        #with app.app_contex():
        mail.send(message)


def send_reset_password_mail(user):
    token = SendMail._get_token(user)
    message = SendMail.email_message(
        'Password reset for Random Pairs Generator',
        'marcin16661@gmail.com',
        [user.email],
        f"""Click the link below to reset your password.
        {url_for(
            'auth.reset_password',
            token=token,
            _external=True
        )}
"""
    )
    SendMail.send_mail(message)
    # app = current_app
    # thread = Thread(target=SendMail.send_mail, args=[app, message])
    # thread.start()
    # return thread


def send_verifiaction_mail(user):
    token = SendMail._get_token(user)
    message = SendMail.email_message(
        'Email confirmation for Random Pairs Generator',
        'plebania@random-pairs-generator.herokuapp.com',
        [user.email],
        f"""Click the link below to confirm your email.
            {url_for(
            'auth.confirm_email',
            token=token,
            _external=True
        )}
    """
    )
    SendMail.send_mail(message)
    # app = current_app
    # with app.app_context():
    #     thread = Thread(target=SendMail.send_mail, args=[message])
    #     thread.start()
    # return thread


def send_mail_to_pairs(recipients):
    for recipient in recipients:
        message = SendMail.email_message(
            'You have been picked',
            recipient['first_person_email'],
            [recipient['second_person_email']],
            'placeholder'
        )
        SendMail.send_mail(message)
