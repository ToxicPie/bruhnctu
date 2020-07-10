import flask
from . import storage
from flask_login import login_required, current_user
import markdown
from markdown.extensions.toc import TocExtension



blueprint = flask.Blueprint('pages', __name__)


flatpages = None

@blueprint.route('/s/<path:path>')
def s(path):
    return storage.get_storage(path)


# home page(s)
@blueprint.route('/')
def index():
    return flask.render_template('index.html')

@blueprint.route('/', methods=['BREW'])
def teapot():
    flask.abort(418)

# @blueprint.route('/about')
# def about():
#     return flask.render_template('about.html')

# flatpages (markdown pages)
@blueprint.route('/<path:path>')
def flatpage(path):
    page = flatpages.get_or_404(path)
    template = page.meta.get('template', 'flatpage.html')
    return flask.render_template(template, page=page)


# website edits
@blueprint.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_page():
    flask.flash('I have not finished this page yet or is simply too lazy.')
    flask.abort(501)

@blueprint.route('/create', methods=['POST'])
@login_required
def create_page():
    flask.flash('I have not finished this page yet or is simply too lazy.')
    flask.abort(501)

@blueprint.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    flask.flash('I have not finished this page yet or is simply too lazy.')
    flask.abort(501)
