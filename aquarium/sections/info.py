from flask import abort, render_template, g
from aquarium import app, utils
import os


def index(path):
    if path == "":
        return render_template('browse.html', output=getScripts('info'))
    if utils.isScript('info/' + path):
        g.title = path
        return render_template('script.html',
            output=utils.tabularToDict(utils.runScript('info/' + path)))
    abort(404)


def getScripts(section):
    root = app.config['AQ_DIR'] + os.sep
    path = section + os.sep
    files = sorted(os.listdir(root + path))
    #  Only use scripts that are executable (X_OK).
    scripts = [x for x in files if utils.isScript(path + x)]
    return scripts
