import flask
from flask_flatpages import FlatPages
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
@app.errorhandler(401)
def error_401(e):
    return flask.render_template('errors/401.html'), 401

@app.errorhandler(403)
def error_403(e):
    return flask.render_template('errors/403.html'), 403

@app.errorhandler(404)
def error_404(e):
    return flask.render_template('errors/404.html'), 404

@app.errorhandler(500)
def error_500(e):
    return flask.render_template('errors/500.html'), 500


if __name__ == '__main__':
    app.run(host = '0.0.0.0')
