import flask
from flask_flatpages import FlatPages
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from os import urandom

app = flask.Flask(__name__)

app.config.from_pyfile('config/flask_config.py')
app.secret_key = urandom(32)



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
