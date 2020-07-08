DEBUG = False
TEMPLATES_AUTO_RELOAD = True
FLATPAGES_MARKDOWN_EXTENSIONS = ['fenced_code', 'codehilite', 'toc', 'components.md_extras']
FLATPAGES_EXTENSION = ['.htm', '.html', '.md']
FLATPAGES_AUTO_RELOAD = True
FLATPAGES_EXTENSION_CONFIGS = {
    'codehilite': {
        'linenums': 'True'
    }
}
