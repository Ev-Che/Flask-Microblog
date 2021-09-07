from flask import current_app, render_template

from app.email import send_email
from app.models import User


def send_password_reset_email(user: User):
    token = user.get_reset_password()
    send_email(subject='[Microblog] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
