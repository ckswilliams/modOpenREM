LOCAL_SETTINGS = True
from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '/home/mcdonaghe/research/openremdev/db.db',                      # Or path to database file if using sqlite3.
        'USER': 'openremuser',                      # Not used with sqlite3.
        'PASSWORD': 'rem',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

