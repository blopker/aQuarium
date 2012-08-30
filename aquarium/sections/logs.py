from flask import render_template
from aquarium import app, utils
import os


def index(path):
    if isLog(path):
        return render_template('log.html',
            output=utils.tabularToDict(readLog('logs/' + path)))
    return render_template('browse.html', output=getLogs())


def readLog(log):
    text = ""
    with open(app.config['AQ_DIR'] + os.sep + log) as l:
        text = l.read()
    return text


def isLog(path):
    return path.split('/')[-1] in getLogs()


def getLogs():
    root = app.config['AQ_DIR'] + os.sep + 'logs'
    files = sorted(os.listdir(root))
    logs = [x for x in files if os.access(root + os.sep + x, os.R_OK)]
    return logs
