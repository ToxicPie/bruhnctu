import flask
from . import storage
from flask_login import login_required


blueprint = flask.Blueprint('pages', __name__)


flatpages = None

@blueprint.route('/s/<path:path>')
def s(path):
    return storage.get_storage(path)


# home page(s)
@blueprint.route('/')
def index():
    flask.flash('hello')
    flask.flash('hello2')
    return flask.render_template('index.html')

@blueprint.route('/about')
def about():
    return flask.render_template('about.html')

# platpages (markdown pages)
@blueprint.route('/<path:path>')
def flatpage(path):
    page = flatpages.get_or_404(path)
    template = page.meta.get('template', 'flatpage.html')
    return flask.render_template(template, page=page)
