from celery import Celery


celery = Celery('EOD_TASKS')
celery.config_from_object('mail_service.gmail_service.celeryconfig')

@celery.task(name='check_account_v1')
def check_account_v1(email, new_history_id, **kwargs):
    pass
