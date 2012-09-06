#!venv/bin/python
from aquarium import app
app.debug = app.config['DEBUG']
app.run(host='0.0.0.0')
