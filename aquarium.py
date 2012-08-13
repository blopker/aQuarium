from flask import Flask, abort, url_for, render_template, g
import os
from collections import OrderedDict
import subprocess

# configuration
SCRIPTS = 'scripts'
DEBUG = True
LOGS = 'logs'

app = Flask(__name__)
app.config.from_object(__name__)


@app.before_request
def before_request():
    g.logs = getLogs()
    g.scripts = getScripts()


@app.route('/')
def index():
    g.title = "Welcome to Aquarium"
    return render_template('index.html')


@app.route('/script/<script>')
def script(script):
    g.title = script
    output = formatScript(runScript(script))
    return render_template('script.html', output=output)


@app.route('/log/<log>')
def log(log):
    g.title = log
    output = formatLog(readLog(log))
    return render_template('log.html', output=output)


@app.errorhandler(500)
def scriptFailed(error):
    return render_template('script.html'), 500


@app.context_processor
def nav():
    nav = {}
    script_nav = {}
    for script in g.scripts:
        script_nav[script] = url_for('script', script=script)
    nav["Scripts"] = script_nav

    logs_nav = {}
    for log in g.logs:
        logs_nav[log] = url_for('log', log=log)
    nav["Logs"] = logs_nav
    return dict(nav=nav)


def getLogs():
    files = sorted(os.listdir(app.config['LOGS']))
    logs = [x for x in files if os.access(app.config['LOGS'] + os.sep + x, os.R_OK)]
    return logs


def readLog(log):
    text = ""
    with open(app.config['LOGS'] + os.sep + log) as l:
        text = l.read()
    return text


def formatScript(string):
    return string.split('\n')


def formatLog(string):
    lists = string.strip().split('\n')
    lists = [lis.strip().split() for lis in lists]
    dic = OrderedDict()

    def mapper(*args):
        dic[args[0]] = args[1:]
    map(mapper, *lists)

    # json_out = json.dumps(dic)
    return dic


def runScript(script):
    if not script in g.scripts:
        abort(501)
    try:
        return subprocess.check_output(app.config['SCRIPTS'] + os.sep + script,
            stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError, e:
        g.error = e.output
        abort(500)


def getScripts():
    files = sorted(os.listdir(app.config['SCRIPTS']))
    #  Only use scripts that are executable (X_OK).
    scripts = [x for x in files if os.access(app.config['SCRIPTS'] + os.sep + x, os.X_OK)]
    return scripts

if __name__ == '__main__':
    app.debug = app.config['DEBUG']
    app.run(host='0.0.0.0')
