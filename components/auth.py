from flask import *
import bcrypt
from urllib.parse import urlparse, urljoin
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from . import forms, database
import logging


blueprint = Blueprint('auth', __name__)

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return database.User.query.get(int(user_id))


# handles '?next=...'
@login_manager.unauthorized_handler
def handle_needs_login():
    flash('Please login to continue.', 'warning')
    return redirect(url_for('auth.login', next=request.full_path))


@blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    logging.info('User {0} (id {1}) has logged out.'.format(current_user.username, current_user.id))

    flash('You have logged out.', 'info')
    return redirect(url_for('pages.index'))

# check if a url is safe for redirect
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return (test_url.scheme in ('http', 'https') and
            ref_url.netloc == test_url.netloc)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():

    def go_next():
        next = request.args.get('next')
        if not is_safe_url(next):
            flash('Bad hacker ...?', 'warning')
            return abort(400)
        return redirect(next or url_for('pages.index'))

    print('start')

    if current_user.is_authenticated:
        flash('You are already logged in!', 'info')
        return go_next()

    form = forms.LoginForm(request.form)
    if not form.validate_on_submit():
        return render_template('login.html', form=form)

    user = database.User.query.filter_by(username=form.username.data).first()

    # check if password matches database
    if not user or not bcrypt.checkpw(form.password.data.encode('ascii'), user.password):
        flash('Error: Invalid credentials, please try again.', 'error')
        return render_template('login.html', form=form)

    login_user(user, remember=form.remember.data)
    logging.info('User {0} (id {1}) has logged in.'.format(current_user.username, current_user.id))

    flash('Welcome, {0}!'.format(current_user.username), 'success')
    return go_next()


@blueprint.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = forms.AccountForm(request.form)

    if not form.validate_on_submit():
        return render_template('account.html', form=form)

    # check password
    user = database.User.query.filter_by(id=current_user.id).first()
    if not user or not bcrypt.checkpw(form.password.data.encode('ascii'), user.password):
        flash('Error: Invalid credentials, please try again.', 'error')
        return render_template('account.html', form=form)

    user_updated = False

    # change username
    if form.new_username.data and form.new_username.data != current_user.username:
        test_user = database.User.query.filter_by(username=form.new_username.data).first()
        if test_user:
            flash('That username is taken.', 'error')
            flash('Nothing was changed.', 'warning')
            return render_template('account.html', form=form)
        else:
            user = database.User.query.filter_by(id=current_user.id).first()
            user.username = form.new_username.data
            user_updated = True

    # change password
    if form.new_password.data:
        hash = bcrypt.hashpw(form.new_password.data.encode('ascii'), bcrypt.gensalt())
        user = database.User.query.filter_by(id=current_user.id).first()
        user.new_password = hash
        user_updated = True

    # is something changed?
    if user_updated:
        database.db.session.commit()
        flash('Your user account has been updated.', 'success')
    else:
        logging.info('User {0} (id {1}) has changed their account.'.format(current_user.username, current_user.id))
        flash('Nothing was changed.', 'warning')

    return redirect(url_for('auth.account'))


# only works in CLI
def add_user(username, password):
    hash = bcrypt.hashpw(password.encode('ascii'), bcrypt.gensalt())
    database.db.session.add(database.User(username=username, password=hash))
    database.db.session.commit()
