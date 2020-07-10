from flask import *
import bcrypt
from urllib.parse import urlparse, urljoin
from flask_login import LoginManager, login_required, login_user, logout_user
from . import forms, database


blueprint = Blueprint('auth', __name__)


login_manager = LoginManager()
login_manager.login_view = 'auth.login_get'
login_manager.login_message = 'Please login to continue.'
login_manager.login_message_category = 'warning'


@login_manager.user_loader
def load_user(user_id):
    return database.User.query.get(int(user_id))


# handles '?next=...'
@login_manager.unauthorized_handler
def handle_needs_login():
    flash('Please login to continue.', 'warning')
    return redirect(url_for('auth.login_get', next=request.full_path))


@blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have logged out.', 'info')
    return redirect(url_for('pages.index'))


@blueprint.route('/login', methods=['POST'])
def login_post():
    form = forms.LoginForm(request.form)
    if not form.validate():
        flash('Invalid form data.', 'warning')
        return abort(400)

    next = request.args.get('next')

    user = database.User.query.filter_by(username=form.username.data).first()

    # check if password matches database
    if not user or not bcrypt.checkpw(form.password.data.encode('ascii'), user.password):
        flash('Invalid credentials, please try again.', 'error')
        return redirect(url_for('auth.login_get', next=next))

    login_user(user, remember=form.remember.data)

    def is_safe_url(target):
        ref_url = urlparse(request.host_url)
        test_url = urlparse(urljoin(request.host_url, target))
        return (test_url.scheme in ('http', 'https') and
                ref_url.netloc == test_url.netloc)

    # check if the url is safe for redirect
    if not is_safe_url(next):
        flash('Bad hacker ...?', 'warning')
        return abort(400)

    flash('You have successfully logged in.', 'info')
    return redirect(next or url_for('pages.index'))


@blueprint.route('/login', methods=['GET'])
def login_get():
    form = forms.LoginForm()
    return render_template('login.html', form=form)


# only works in CLI
def add_user(username, password):
    hash = bcrypt.hashpw(password.encode('ascii'), bcrypt.gensalt())
    database.db.session.add(database.User(username=username, password=hash))
    database.db.session.commit()
