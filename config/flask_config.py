DEBUG = False
TEMPLATES_AUTO_RELOAD = True

FLATPAGES_MARKDOWN_EXTENSIONS = ['fenced_code', 'codehilite', 'toc', 'components.md_extras']
FLATPAGES_EXTENSION = ['.htm', '.html', '.md']
FLATPAGES_AUTO_RELOAD = True
FLATPAGES_EXTENSION_CONFIGS = {
    'codehilite': {
        'linenums': 'True',
        'guess_lang': 'False'
    },
    'toc': {
        'toc_depth': '2-2'
    }
}

SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'

REMEMBER_COOKIE_HTTPONLY = True
REMEMBER_COOKIE_DURATION = 604800  # 7 days
