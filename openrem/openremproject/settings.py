# Django settings for OpenREM project.

from __future__ import absolute_import
# ^^^ The above is required if you want to import from the celery
# library.  If you don't have this then `from celery.schedules import`
# becomes `proj.celery.schedules` in Python 2.x since it allows
# for relative imports by default.
from celery.schedules import crontab
import os


# Debug is now set to false - you can turn it back on in local_settings if you need to
DEBUG = False
TEMPLATE_DEBUG = False

# Celery settings
BROKER_URL = 'amqp://guest:guest@localhost//'
CELERY_RESULT_BACKEND = 'rpc://'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_DEFAULT_QUEUE = 'default'

CELERY_ACKS_LATE = True
CELERYD_PREFETCH_MULTIPLIER = 1


CELERYBEAT_SCHEDULE = {
    'trigger-dicom-keep-alive': {
        'task': 'remapp.netdicom.keepalive.keep_alive',
        'schedule': crontab(minute='*/1'),
        'options': {'expires': 10},  # expire if not run ten seconds after being scheduled
    },
}


ROOT_PROJECT = os.path.join(os.path.split(__file__)[0], "..")

# **********************************************************************
#
# Database settings have been moved to local_settings.py
# Line below will be overwritten there. Included here for docs issue
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'openrem.db', 'USER': '', 'PASSWORD': '', 'HOST': '', 'PORT': '', }}
#
# **********************************************************************

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Default date and time format for exporting to Excel xlsx spreadsheets - use Excel codes, override it in local_settings.py
XLSX_DATE = 'dd/mm/yyyy'
XLSX_TIME = 'hh:mm:ss'

#
# MEDIA_ROOT filepath has been moved to local_settings.py
# Line below will be overwritten there. Included here for docs issue
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
# MEDIA_URL = '/media/'

#
# STATIC_ROOT filepath has been moved to local_settings.py
#

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(ROOT_PROJECT, 'remapp', 'static'),
)

#
# SECRET_KEY must be changed in local_settings.py
#
SECRET_KEY = 'youmustchangethiskeyinlocal_settings'

# URL name of the login page (as defined in urls.py)
LOGIN_URL = 'login'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',  # Added by ETM
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'openremproject.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'openremproject.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'remapp',
    'django_filters',
    'pagination',
    'django.contrib.humanize',
    'solo',
    'crispy_forms',
    'debug_toolbar',
    'django_js_reverse'
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'openrem.log',
            'formatter': 'verbose'
        },
        'qr_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'openrem_qrscu.log',
            'formatter': 'verbose'
        },
        'store_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'openrem_storescp.log',
            'formatter': 'verbose'
        },
        'extractor_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'openrem_extractor.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'remapp': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'remapp.netdicom.qrscu': {
            'handlers': ['qr_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'remapp.netdicom.storescp': {
            'handlers': ['store_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'remapp.extractors.ct_toshiba': {
            'handlers': ['extractor_file'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

# Dummy locations of various tools for DICOM RDSR creation from CT images. Don't set value here - copy variables into
# # local_settings.py and configure there.
DCMTK_PATH = ''
DCMCONV = os.path.join(DCMTK_PATH, 'dcmconv.exe')
DCMMKDIR = os.path.join(DCMTK_PATH, 'dcmmkdir.exe')
JAVA_EXE = ''
JAVA_OPTIONS = '-Xms256m -Xmx512m -Xss1m -cp'
PIXELMED_JAR = ''
PIXELMED_JAR_OPTIONS = '-Djava.awt.headless=true com.pixelmed.doseocr.OCR -'

# Dummy variable for running the website in a virtual_directory. Don't set value here - copy variable into
# local_settings.py and configure there.
VIRTUAL_DIRECTORY = ''

# E-mail server settings - see https://docs.djangoproject.com/en/1.8/topics/email/
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'a.user.that.can.send'
EMAIL_HOST_PASSWORD = 'the.above.user.password'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
EMAIL_DOSE_ALERT_SENDER = 'your.alert@email.address'
EMAIL_OPENREM_URL = 'http://your.openrem.server'

try:
    LOCAL_SETTINGS
except NameError:
    try:
        from openremproject.local_settings import *
    except ImportError:
        try:
            from openrem.openremproject.local_settings import *
        except ImportError:
            pass
