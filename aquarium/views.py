from flask import abort, render_template, g
from aquarium import app
import os
from collections import OrderedDict
import subprocess

# configuration
AQ_DIR = 'test_dir'
# AQ_DIR = 'aq_dir'
DEBUG = True

app.config.from_object(__name__)


@app.before_request
def before_request():
    g.url_path = "/"
    g.sections = getSections()
    # g.logs = getLogs()
    # g.scripts = getScripts()


# @app.route('/')
# def index():
#     g.title = "Welcome to Aquarium"
#     return render_template('index.html')

@app.route('/')
# @app.route('/<path:path>')
def index():
    g.title = "Home"
    g.url_path = '/'
    return render_template('index.html', data=runScript('index.sh'))


@app.route('/<sec>/', defaults={'path': ""})
@app.route('/<sec>/<path:path>')
def section(sec, path):
    g.section = sec
    g.title = sec
    g.url_path = '/' + sec
    try:
        return globals()["section_" + sec](path)
    except KeyError:
        return abort(404)


def section_logs(path):
    if isLog(path):
        return render_template('log.html', output=tabularToDict(readLog('logs/' + path)))
    return render_template('browse.html', output=getLogs())


def section_scripts(path):
    if path == "":
        return render_template('browse.html', output=getScripts())
    if isScript(path):
        return render_template('script.html', output=tabularToDict(runScript('scripts/' + path)))
    abort(404)

# def getParent(path):
#     return '/'.join(path.rstrip('/').split('/')[:-1]) + '/'


# def isFile(path):
#     return os.path.isfile(app.config['AQ_DIR'] + os.sep + path)


def isDir(path):
    return os.path.isdir(app.config['AQ_DIR'] + os.sep + path)


# def showFile(file):
#     output = tabularToDict(readLog(file))
#     return render_template('log.html', output=output)


# def showDir(dir):
#     g.dirs, g.files = getContents(dir)
#     return render_template('index.html')

# @app.route('/<path:path>')
# def view(path):
#     g.title = path.split("/")[-1]
#     return "hello"

# @app.route('/scripts/', defaults={'path': "/"})
# @app.route('/scripts<path:path>')
# def scripts(path):
#     g.title = "Scripts"
#     output = g.scripts
#     return render_template('browse.html', output=output, type="script")


# @app.route('/script/<file>')
# def script(file):
#     g.title = file
#     output = tabularToDict(runScript(file))
#     return render_template('script.html', output=output)


# @app.route('/logs/', defaults={'path': "/"})
# @app.route('/logs<path:path>')
# def logs(path):
#     g.title = "Logs"
#     output = g.logs
#     return render_template('browse.html', output=output, type="log")


# @app.route('/log/<file>')
# def log(file):
#     g.title = file
#     output = tabularToDict(readLog(file))
#     return render_template('log.html', output=output)


# @app.errorhandler(500)
# def scriptFailed(error):
#     return render_template('script.html'), 500


def getLogs():
    root = app.config['AQ_DIR'] + os.sep + 'logs'
    files = sorted(os.listdir(root))
    logs = [x for x in files if os.access(root + os.sep + x, os.R_OK)]
    return logs


def readLog(log):
    text = ""
    with open(app.config['AQ_DIR'] + os.sep + log) as l:
        text = l.read()
    return text


# def formatScript(string):
#     return string.split('\n')


def tabularToDict(string):
    lists = string.strip().split('\n')
    lists = [lis.strip().split() for lis in lists]
    dic = OrderedDict()

    def mapper(*args):
        dic[args[0]] = args[1:]
    map(mapper, *lists)

    return dic


def runScript(script):
    try:
        return subprocess.check_output(app.config['AQ_DIR'] + os.sep + script,
            stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError, e:
        g.error = e.output
        abort(500)


def getSections():
    root = app.config['AQ_DIR']
    contents = os.listdir(root)
    dirs = sorted([x for x in contents if os.path.isdir(root + os.sep + x)])
    return dirs


def isScript(path):
    root = app.config['AQ_DIR'] + os.sep
    if isDir(root + path):
        return False
    return os.access(root + path, os.X_OK)


def isLog(path):
    return path.split('/')[-1] in getLogs()


def getScripts():
    root = app.config['AQ_DIR'] + os.sep
    path = 'scripts' + os.sep
    files = sorted(os.listdir(root + path))
    print files
    #  Only use scripts that are executable (X_OK).
    scripts = [x for x in files if isScript(path + x)]
    print scripts
    return scripts
