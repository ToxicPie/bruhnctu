from flask import *
from . import storage
from . import auth
from . import forms
from flask_login import login_required, current_user
import os
from os import path
import re
from hashlib import md5
import markdown
from markdown.extensions.toc import TocExtension



blueprint = Blueprint('pages', __name__)


flatpages = None

@blueprint.route('/s/<path:path>')
def s(path):
    return storage.get_storage(path)


# home page(s)
@blueprint.route('/')
def index():
    return render_template('index.html')

@blueprint.route('/', methods=['BREW'])
def teapot():
    abort(418)

# @blueprint.route('/about')
# def about():
#     return render_template('about.html')

# flatpages (markdown pages)
@blueprint.route('/<path:path>')
def flatpage(path):
    page = flatpages.get_or_404(path)

    # check permissions t view the page
    login_required = page.meta.get('login_required', False)
    if login_required:
        if not current_user.is_authenticated:
            return auth.handle_needs_login()

    template = str(page.meta.get('template', 'default'))
    if template == 'default':
        template = 'markdown.html'
    elif not template.endswith('.html'):
        template += '.html'

    return render_template(template, page=page)


# website edits
@blueprint.route('/editpage', methods=['GET', 'POST'])
@login_required
def edit_page():
    form = forms.EditPageForm(request.form)

    if form.path.data == '':
        form.path.data = request.args.get('path')

    orig_file_contents = ''
    # safe ...?
    if re.match(r'^[a-zA-Z0-9_/]{3,50}$', form.path.data):
        filename = path.normpath('pages/' + form.path.data) + '.md'
        if path.isfile(filename):
            orig_file_contents = open(filename, 'r').read()

    if not form.validate_on_submit():
        form.content.data = orig_file_contents
        if orig_file_contents != '':
            flash('File {0} has been loaded.'.format(form.path.data + '.md'), 'info')
        return render_template('edit-page.html', form=form)

    if not form.save_file.data:
        form.content.data = orig_file_contents
        if orig_file_contents != '':
            flash('File {0} has been loaded.'.format(form.path.data + '.md'), 'info')
    else:
        filename = path.normpath('pages/' + form.path.data) + '.md'

        if not path.isfile(filename):
            # new file
            os.makedirs(path.dirname(filename), exist_ok=True)
            with open(filename, 'w') as file:
                file.write(form.content.data)
            flash('Page {0} has been created.'.format(form.path.data), 'success')
        else:
            # existing file
            # create backup
            orig_file_contents = open(filename, 'rb').read()
            hash = md5(orig_file_contents).hexdigest()[:6]
            new_file = path.normpath('files/backup/pages/' + form.path.data) + '-' + hash + '.md'
            os.makedirs(path.dirname(new_file), exist_ok=True)
            with open(new_file, 'wb') as file:
                file.write(orig_file_contents)
            # update file
            with open(filename, 'w') as file:
                file.write(form.content.data)
            flash('Page {0} has been updated.'.format(form.path.data), 'success')

    return render_template('edit-page.html', form=form)


@blueprint.route('/createpage', methods=['POST'])
@login_required
def create_page():
    flash('I have not finished this function yet.')
    abort(501)

@blueprint.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    flash('I have not finished this function yet.')
    abort(501)
