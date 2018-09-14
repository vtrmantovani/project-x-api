from requests.exceptions import ConnectTimeout
from sqlalchemy.exc import SQLAlchemyError

from pxa import celery, db, logger
from pxa.backends.website import WebsiteBackend
from pxa.models.website import Website
from pxa.tasks.exceptions import TasksException


@celery.task(name='task.process_available_links',
             queue='pxa.website',
             bind=True,
             max_retries=3)
def process_available_links(self, website_id):

    logger.info("Task to process available links: started. website_id={0}".format(website_id))  # noqa

    try:
        website = Website.query.filter(Website.id == website_id).first()

        if not website:
            logger.error("Task to process available links: website not found. website_id={0}".format(website_id))  # noqa
            raise TasksException('Website not found: website_id={0}'.format(website_id))  # noqa

        WebsiteBackend().save_website_available_links(website)

    except ConnectTimeout as exc:
        self.retry(exc=exc, countdown=180)
    except SQLAlchemyError as exc:
        db.session.rollback()
        self.retry(exc=exc, countdown=180)
    except TasksException as e:
        raise TasksException(str(e))
    except Exception as e:
        logger.exception("Task to process available links: exception. website_id={0}".format(website_id))  # noqa

        if website:
            WebsiteBackend().failed_save_website_available_links(website, str(e))  # noqa

    logger.info("Task to process available links: ended. website_id={0}".format(website_id))  # noqa
