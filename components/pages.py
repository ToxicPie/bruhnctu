import flask
from . import storage
from flask_login import login_required
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

@blueprint.route('/about')
def about():
    return flask.render_template('about.html')

# flatpages (markdown pages)
@blueprint.route('/<path:path>')
def flatpage(path):
    page = flatpages.get_or_404(path)
    # text = open('pages/' + path + '.md', 'r').read()
    # md = markdown.Markdown(extensions=[TocExtension(toc_depth="2-2")])
    # md.convert(text)
    # return md.toc
    template = page.meta.get('template', 'flatpage.html')
    return flask.render_template(template, page=page)
