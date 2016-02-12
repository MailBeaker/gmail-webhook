import os

DEBUG = os.getenv('DEBUG', False)

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

SPLUNK_HOST = os.getenv('SPLUNK_HOST', 'splunk.example.com')
SPLUNK_PORT = os.getenv('SPLUNK_PORT', '8089')
SPLUNK_USERNAME = os.getenv('SPLUNK_USERNAME', 'admin')
SPLUNK_PASSWORD = os.getenv('SPLUNK_PASSWORD', 'changeme')
SPLUNK_INDEX = os.getenv('SPLUNK_INDEX', 'main')
SPLUNK_HOSTNAME = os.getenv('SPLUNK_HOSTNAME', 'gmail-webhook.mailbeaker.dev')
SPLUNK_VERIFY = os.getenv('SPLUNK_VERIFY', 'True')
SPLUNK_VERIFY = False if SPLUNK_VERIFY == 'False' else True

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(created)f %(exc_info)s %(filename)s %(funcName)s %(levelname)s %(levelno)s %(lineno)d %(module)s %(message)s %(pathname)s %(process)s %(processName)s %(relativeCreated)d %(thread)s %(threadName)s'
        },
        'verbose': {
            'format': 'levelname=%(levelname)s asctime=%(asctime)s module=%(module)s process=%(process)d thread=%(thread)d message="%(message)s"'
        }
    },
    'handlers': {
        'splunk': {
            'level': LOG_LEVEL,
            'class': 'splunk_handler.SplunkHandler',
            'formatter': 'json',
            'host': SPLUNK_HOST,
            'port': SPLUNK_PORT,
            'username': SPLUNK_USERNAME,
            'password': SPLUNK_PASSWORD,
            'index': SPLUNK_INDEX,
            'hostname': SPLUNK_HOSTNAME,
            'sourcetype': 'json',
            'verify': SPLUNK_VERIFY
        },
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'splunk'],
            'level': LOG_LEVEL
        }
    }
}


try:
    from settingslocal import *
except ImportError:
    pass
