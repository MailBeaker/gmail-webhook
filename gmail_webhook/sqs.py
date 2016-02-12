from mail_service.gmail_service.worker import check_account_v1
import datetime
import json
import logging
import settings

log = logging.getLogger(__name__)

class SqsBroker():
    """
    Post items to an Amazon SQS queue.
    """
    def post_to_queue(self, message):
        """
        Actually post a message to the queue.

        :param message: the dict being posted the the SQS queue.
        """
        log.info('Call to post_to_queue()', extra = {
            'payload': message
        })

        if not 'emailAddress' in message or not 'historyId' in message:
            raise ValueError("Message payload did not validate.")

        now = datetime.datetime.now()
        check_account_v1.delay(message['emailAddress'], message['historyId'], queue_time=now)
