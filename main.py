from logging import config
from flask import Flask

import settings
from gmail_webhook import sqs

# Setup logging
config.dictConfig(settings.LOGGING)

sqs_broker = sqs.SqsBroker()

# Creating the Flask app object
app = Flask(__name__)
app.debug = settings.DEBUG

from gmail_webhook import views
