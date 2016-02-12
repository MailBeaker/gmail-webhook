import unittest
import json

import mock
from flask import url_for
from gmail_webhook import sqs

from main import app

GMAIL_DATA = 'eyJlbWFpbEFkZHJlc3MiOiAidXNlckBleGFtcGxlLmNvbSIsICJoaXN0b3J5SWQiOiAiMTIzNDU2Nzg5MCJ9'

class ViewsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    @mock.patch('gmail_webhook.views.sqs_broker')
    def test_receive(self, sqs_broker):
        payload = {
            'message': {
                'data': GMAIL_DATA,
                'message_id': '1234567890'
            },
            'subscription': 'test/path/stuff'
        }

        rv = self.app.post(
            '/receive',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(payload))

        sqs_broker.post_to_queue.assert_called_with({
            'emailAddress': 'user@example.com',
            'historyId': '1234567890'})

        assert 201 == rv.status_code

    @mock.patch('gmail_webhook.views.sqs_broker')
    def test_receive_no_data(self, sqs_broker):
        payload = {
            'message': {
                'message_id': '1234567890'
            },
            'subscription': 'test/path/stuff'
        }

        rv = self.app.post(
            '/receive',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(payload))

        assert 400 == rv.status_code

    @mock.patch('gmail_webhook.views.sqs_broker')
    def test_receive_no_email_address(self, sqs_broker):
        payload = {
            'message': {
                # {"historyId": "1234567890"}
                'data': 'eyJoaXN0b3J5SWQiOiAiMTIzNDU2Nzg5MCJ9',
                'message_id': '1234567890'
            },
            'subscription': 'test/path/stuff'
        }

        sqs_broker.post_to_queue.side_effect = ValueError()

        rv = self.app.post(
            '/receive',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(payload))

        assert 400 == rv.status_code

    @mock.patch('gmail_webhook.views.sqs_broker')
    def test_receive_no_history_id(self, sqs_broker):
        payload = {
            'message': {
                # {"emailAddress": "user@example.com"}
                'data': 'eyJlbWFpbEFkZHJlc3MiOiAidXNlckBleGFtcGxlLmNvbSJ9',
                'message_id': '1234567890'
            },
            'subscription': 'test/path/stuff'
        }

        sqs_broker.post_to_queue.side_effect = ValueError()

        rv = self.app.post(
            '/receive',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(payload))

        assert 400 == rv.status_code
