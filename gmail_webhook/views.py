import json
import logging
import os
import base64

from flask import abort,request,url_for
from flask.views import MethodView

from main import app

from main import sqs_broker

log = logging.getLogger(__name__)

class ReceiveView(MethodView):
    """
    Receives the webhook
    """

    def post(self):
        req = request.get_json()

        log.info('', extra = {
            'view': 'receive',
            'payload': req
        })

        try:
            sqs_broker.post_to_queue(decode_data(req['message']['data']))
        except KeyError:
            log.exception('Missing key in request')
            abort(400)
        except ValueError:
            log.exception('Data format incorrect')
            abort(400)
        except:
            log.exception('Unexpected exception')
            abort(500)

        return ('', 201)


def decode_data(data):
    data_string = base64.b64decode(data).decode('utf-8')
    return json.loads(data_string)



###########
# URL Rules
###########

app.add_url_rule('/receive', view_func=ReceiveView.as_view('receive'))
