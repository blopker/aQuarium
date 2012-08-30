from flask import abort, render_template, g, request
from aquarium import app, utils


class AjaxScript():
    """Represents an ajax script with check and call endpoints"""
    def __init__(self, name, runURL, checkURL=""):
        self.name = name
        self.checkURL = checkURL
        self.runURL = runURL


def index(path):
    if request.method == 'POST':
        return utils.runScript('nsman/' + path)
    scripts = [AjaxScript('Sleep5', '/nsman/sleep5.sh')]
    return render_template('ajax.html', output=scripts)
