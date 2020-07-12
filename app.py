import flask
from flask_flatpages import FlatPages
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy


app = flask.Flask(__name__)

app.config.from_pyfile('config/flask_config.py')
# generated from os.urandom(24)
app.secret_key = b'\x03\xbc\xde\xef\x9c\x35\x98\x92\x50\x07\x0f\x2e\x25\xe5\x9a\x61\xa5\x4c\x5f\x43\x64\x7f\xa9\x59'



from components import pages, exceptions, auth

pages.flatpages = FlatPages(app)
auth.database.db = SQLAlchemy(app)
# auth.database.db.init_app(app)
auth.login_manager.init_app(app)
csrf = CSRFProtect()
csrf.init_app(app)

app.register_blueprint(pages.blueprint)
app.register_blueprint(exceptions.blueprint)
app.register_blueprint(auth.blueprint)


if __name__ == '__main__':
    app.run(host = '0.0.0.0')
