import flask


files = {
    'exam1.pdf': (
        False,
        '31755f83b0be799d201d42290914964f',
        '/home/kent/git/CP1-Exam/2020-Spring/midterm1/tex/main.pdf'
    ),
    'ai_report.pdf': (
        False,
        'dc07fc3b76c1a4a516d93a3ad11ab1f1',
        '/home/kent/Downloads/hw/ai/group/report/report.pdf'
    )
}


def get_file(path, token):
    if path in files:
        if files[path][0] and token == files[path][1]:
            return flask.send_file(files[path][2])
        else:
            flask.abort(401)
    else:
        flask.abort(404)
