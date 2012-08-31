from flask import g
from aquarium import app
import os
import subprocess


def tabularToDict(string):
    lists = string.strip().split('\n')
    lists = [lis.strip().split() for lis in lists]
    dic = {}

    def mapper(*args):
        dic[args[0]] = args[1:]
    map(mapper, *lists)

    return dic


def isDir(path):
    return os.path.isdir(app.config['AQ_DIR'] + os.sep + path)


def runScript(script):
    try:
        return subprocess.check_output(app.config['AQ_DIR'] + os.sep + script,
            stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError, e:
        g.error = e.output
        return e.output


def isScript(path):
    root = app.config['AQ_DIR'] + os.sep
    if isDir(root + path):
        return False
    return os.access(root + path, os.X_OK)
