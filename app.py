import flask
from flask_flatpages import FlatPages
from werkzeug.exceptions import HTTPException
import logging

import components



app = flask.Flask(__name__)

app.config.from_pyfile('config/flask_config.py')
app.secret_key = b'\x03\xbc\xde\xef\x9c\x35\x98\x92\x50\x07\x0f\x2e\x25\xe5\x9a\x61\xa5\x4c\x5f\x43\x64\x7f\xa9\x59' # generated from os.urandom(24)
flatpages = FlatPages(app)


@app.route('/s/<path:path>')
def s(path):
    return components.code_storage.get_storage(path)


# home page(s)
@app.route('/')
def root():
    return flask.render_template('index.html')

@app.route('/about')
def about():
    return flask.render_template('about.html')

# @app.route('/codebook')
# def codebook():
#     return flask.send_file('/home/kent/git/codebook/codebook.pdf')


# platpages (markdown)
@app.route('/<path:path>')
def flatpage(path):
    page = flatpages.get_or_404(path)
    template = page.meta.get('template', 'flatpage.html')
    return flask.render_template(template, page=page)


# error handlers
@app.errorhandler(Exception)
def on_error(e):
    if isinstance(e, HTTPException):
        error_code = e.code
    else:
        # not http error, log to file
        logging.exception("Internal server error")
        error_code = 500

    ERROR_MSGS = {
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        500: "Internal Server Error",
    }
    error_msg = ERROR_MSGS.get(error_code, 'Unhandled error')
    return flask.render_template('error.html',
                                 code=error_code,
                                 message=error_msg), error_code


if __name__ == '__main__':
    app.run(host = '0.0.0.0')
