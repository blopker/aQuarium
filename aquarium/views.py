from flask import abort, render_template, g
from aquarium import app, utils
import os
import importlib

# configuration
AQ_DIR = 'test_dir'
# AQ_DIR = 'aq_dir'
DEBUG = True
VERSION = '0.1'

app.config.from_object(__name__)


@app.before_request
def before_request():
    # Set all the globals the templates are expecting.
    g.version = app.config['VERSION']
    g.url_path = "/"
    g.sections = getSections()
    g.title = ""
    g.section = ""


@app.route('/')
def index():
    g.title = "Home"
    g.url_path = '/'
    return render_template('index.html', data=utils.runScript('index.sh'))


@app.route('/<sec>/', defaults={'path': ""}, methods=['GET', 'POST'])
@app.route('/<sec>/<path:path>', methods=['GET', 'POST'])
def section(sec, path):
    g.section = sec
    g.title = sec
    g.url_path = '/' + sec
    try:
        mod = importlib.import_module('aquarium.sections.' + sec)
        return mod.index(path)
    except ImportError:
        return abort(404)


def getSections():
    root = app.config['AQ_DIR']
    contents = os.listdir(root)
    dirs = sorted([x for x in contents if os.path.isdir(root + os.sep + x)])
    return dirs
