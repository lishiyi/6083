import os
basedir = os.path.abspath(os.path.dirname(__file__))

WHOOSH_BASE = os.path.join(basedir, 'search.db')
MAX_SEARCH_RESULTS = 50
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
