import os
import pygments
from pygments import lexers, formatters
import flask


FILE_PATH_PREFIX = 'files/storage'


def get_html_cached(filename):
    file_path = os.path.join(FILE_PATH_PREFIX, filename)
    cache_path = os.path.join('files/storage_cache', filename + '.html')

    # has updated cache
    if (os.path.isfile(cache_path) and
        os.path.getmtime(cache_path) > os.path.getmtime(file_path)):

        with open(cache_path, "r") as cache:
            return cache.read()

    else:

        lexer = pygments.lexers.get_lexer_for_filename(file_path)
        formatter = pygments.formatters.HtmlFormatter(linenos='table')

        with open(file_path, 'r') as file:
            html = pygments.highlight(file.read(), lexer, formatter)

        # create or update cache
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        with open(cache_path, "w") as cache:
            cache.write(html)

        return html


def render_code(filename, force_raw):

    file_path = os.path.join(FILE_PATH_PREFIX, filename)

    # pretty version requested
    if 'pretty' in flask.request.args:

        html = get_html_cached(filename)
        # is dark theme requested
        dark = 'dark' in flask.request.args
        # html title
        title = os.path.basename(file_path)

        return flask.render_template('code/code.html', trim_blocks=True, dark=dark, title=title, html=flask.Markup(html))

    # return plaintext version otherwise
    else:
        result = flask.send_from_directory(FILE_PATH_PREFIX, filename)

        # set browser to display paintext unless otherwise specified
        if flask.request.args.get('raw') == 'false' and not force_raw:
            headers = { }
        else:
            headers = { 'Content-Type': 'text/plain; charset=utf-8' }

        return result, 200, headers



# path handlers below

def get_storage(path):
    # get file from path requested
    full_path = os.path.join(FILE_PATH_PREFIX, path)

    if not os.path.isfile(full_path):
        flask.abort(404)

    # print requested file
    return render_code(path, force_raw=False)
