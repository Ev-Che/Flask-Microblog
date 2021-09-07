from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app.auth import bp
from app.auth.email import send_password_reset_email
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
from app.services import get_user_by_username, add_user_to_db, get_user_by_email, update_user_password

from flask_babel import _, lazy_gettext as _l


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_username(form.username.data)

        if user is None or not user.check_password(form.password.data):
            flash(_l('Invalid username or password'))
            return redirect(url_for('auth.login'))

        login_user(user=user, remember=form.remember_me.data)
        next_page = _get_next_page()
        return redirect(next_page)

    return render_template('auth/login.html', title='Sign In',
                           form=form)


def _get_next_page():
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('main.index')
    return next_page


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        _register_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', title='Register',
                           form=form)


def _register_user(username, email, password):
    add_user_to_db(username=username,
                   email=email,
                   password=password)
    flash(_l('Congratulations, you are now a registered user!'))


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = ResetPasswordRequestForm()

    if form.validate_on_submit():
        user = get_user_by_email(email=form.email.data)
        if user:
            send_password_reset_email(user)
        flash(_l('Check your email for the instructions to reset your password'))
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token: str):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token=token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        update_user_password(user=user, password=form.password.data)
        flash(_l('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
