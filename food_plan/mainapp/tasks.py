from celery import shared_task


@shared_task()
def celery_test():
    """Sends an email when the feedback form has been submitted."""
    print("I'm working!")
