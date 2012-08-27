from flask import abort, render_template
from aquarium import app, utils
import os


def index(path):
    if path == "":
        return render_template('browse.html', output=getScripts())
    if isScript('scripts/' + path):
        return render_template('script.html',
            output=utils.tabularToDict(utils.runScript('scripts/' + path)))
    abort(404)


def getScripts():
    root = app.config['AQ_DIR'] + os.sep
    path = 'scripts' + os.sep
    files = sorted(os.listdir(root + path))
    #  Only use scripts that are executable (X_OK).
    scripts = [x for x in files if isScript(path + x)]
    return scripts


def isScript(path):
    root = app.config['AQ_DIR'] + os.sep
    if utils.isDir(root + path):
        return False
    return os.access(root + path, os.X_OK)
