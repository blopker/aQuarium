from flask import abort, render_template, g, request
from aquarium import app, utils
import os


class AjaxScript():
    """Represents an ajax script with check and call endpoints"""
    def __init__(self, name, runURL, checkURL=""):
        self.name = name
        self.checkURL = checkURL
        self.runURL = runURL


def index(path):
    if request.method == 'POST':
        resp = utils.runScript('controls/' + path).replace('\n', '<br/>')
        return resp
    return render_template('ajax.html', output=getControls())


def getAllFiles(path):
    ans = []
    for root, dirs, files in os.walk(path):
        for file in files:
            r = root.split(path)
            r = r[1].strip(os.sep)
            ans.append(r + os.sep + file)
    return ans


def getControls():
    root = app.config['AQ_DIR'] + '/controls/'
    dir = {}
    sections = [x for x in os.listdir(root) if os.path.isdir(root + x)]
    for section in sections:
        ls = []
        for file in getAllFiles(root + section):
            ls.append(AjaxScript(file.strip(os.sep), '/controls/' + section + file))
        dir[section] = ls
    return dir
