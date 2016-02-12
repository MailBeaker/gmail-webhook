import unittest
import json

import mock
from gmail_webhook import sqs

class SqsTestCase(unittest.TestCase):
    def setUp(self):
        self.broker = sqs.SqsBroker()

    def tearDown(self):
        self.broker = None

    @mock.patch('mail_service.gmail_service.worker.check_account_v1.delay')
    def test_post_to_queue(self, delay):
        self.broker.post_to_queue({
            'emailAddress': 'test@example.com',
            'historyId': '1234567890'
        })

        delay.assert_called_once_with('test@example.com', '1234567890', queue_time=mock.ANY)

    def test_post_to_queue_no_history(self):
        with self.assertRaises(ValueError):
            self.broker.post_to_queue({
                'emailAddress': 'test@example.com'
            })


    def test_post_to_queue_no_email(self):
        with self.assertRaises(ValueError):
            self.broker.post_to_queue({
                'historyId': '1234567890'
            })


