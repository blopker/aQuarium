from flask import Flask, abort, url_for, render_template, redirect
import os
import subprocess

# configuration
SCRIPTS = 'scripts'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<command>')
def command(command):
    output = formatString(runCommand(command))
    return render_template('output.html', output=output, command=command)


@app.route('/commands')
def commands():
    return redirect(url_for('index'))


@app.context_processor
def nav():
    nav = {}
    commands = getCommands()
    for cmd in commands:
        nav[cmd] = url_for('command', command=cmd)
    return dict(nav=nav)


def formatString(string):
    return string.split('\n')


def runCommand(command):
    script = getScriptName(command)
    if script:
        return runScript(script)
    abort(501)


def runScript(script):
    try:
        return subprocess.check_output(app.config['SCRIPTS'] + os.sep + script,
            stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        abort(500)


def getScriptName(command):
    commands = getCommands()
    if command in commands:
        return commands[command]
    return ""


def getCommands():
    commands = {}
    scripts = getScripts()
    for script in scripts:
        # command = script.split('.')[0]
        command = script
        commands[command] = script
    return commands


def getScripts():
    files = sorted(os.listdir(app.config['SCRIPTS']))
    scripts = [x for x in files if os.access(app.config['SCRIPTS'] + os.sep + x, os.X_OK)]
    return scripts

if __name__ == '__main__':
    app.debug = app.config['DEBUG']
    app.run(host='0.0.0.0')
