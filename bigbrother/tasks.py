import celery
from .core import update_modules

@celery.task(ignore_result=True)
def update_bigbrother():
    logger = update_bigbrother.get_logger()

    logger.info('Updating BigBrother modules...')
    update_modules()
    logger.info('Update complete.')