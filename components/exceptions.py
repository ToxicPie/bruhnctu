import flask
from werkzeug.exceptions import HTTPException
from flask_wtf.csrf import CSRFError
from .http_statuses import HTTP_STATUSES
import logging


blueprint = flask.Blueprint('exceptions', __name__)


# error handler
@blueprint.app_errorhandler(Exception)
def on_error(e):
    logging.exception(e)
    if isinstance(e, CSRFError):
        flask.flash('Invalid CSRF token.', 'error')
        error_code = 400
    elif isinstance(e, HTTPException):
        error_code = e.code
    else:
        error_code = 500

    error_msg = HTTP_STATUSES.get(error_code, 'Unknown error')
    
    if error_code == 500:
        flask.flash('Unexpected error! Please contact the admin so he can panic.', 'error')

    return flask.render_template('error.html',
                                 code=error_code,
                                 message=error_msg), error_code
