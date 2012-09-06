#!venv/bin/python
from wsgiref.handlers import CGIHandler
from aquarium import app

CGIHandler().run(app)
