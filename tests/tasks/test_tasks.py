from datetime import datetime

import mock
import vcr
from freezegun import freeze_time
from requests.exceptions import ConnectTimeout
from sqlalchemy.exc import SQLAlchemyError

from pxa import db
from pxa.models.website import Website
from pxa.tasks import (process_available_links,
                       retry_process_available_links_processing,
                       website_processing)
from pxa.tasks.exceptions import TasksException
from tests.base import BaseTestCase


class TestTasks(BaseTestCase):

    def setUp(self):
        super(TestTasks, self).setUp()

    def load_fixtures(self):
        website = Website()
        website.url = "http://vtrmantovani.com.br"
        website.status = Website.Status.NEW
        db.session.add(website)
        db.session.commit()

    @mock.patch('pxa.backends.website.WebsiteBackend._save_website_links')
    def test_process_available_links(self, mock_save_website):
        self.assertEqual(Website.query.count(), 1)
        with vcr.use_cassette('tests/fixtures/cassettes/test_process_available_links.yaml'):  # noqa
            process_available_links(1)

        website_db = Website.query.filter(Website.id == 1).first()  # noqa

        self.assertEqual(website_db.status.value, "DONE")

    def test_process_available_links_web_site_not_found(self):
        with self.assertRaises(TasksException) as error:
            process_available_links(2)

        self.assertEqual(str(error.exception), "Website not found: website_id=2")  # noqa

    @mock.patch('pxa.backends.website.WebsiteBackend.save_website_available_links')  # noqa
    def test_process_available_links_connect_timeout(self, mock_response):
        mock_response.side_effect = mock.Mock(side_effect=ConnectTimeout())
        with self.assertRaises(ConnectTimeout):
            process_available_links(1)

        self.assertEqual(mock_response.call_count, 1)

    @mock.patch('pxa.backends.website.WebsiteBackend.save_website_available_links')  # noqa
    def test_process_available_links_sqlalchemy_error(self, mock_response):
        mock_response.side_effect = mock.Mock(side_effect=SQLAlchemyError())
        with self.assertRaises(SQLAlchemyError):
            process_available_links(1)

        self.assertEqual(mock_response.call_count, 1)

    @mock.patch('pxa.backends.website.WebsiteBackend.save_website_available_links')  # noqa
    def test_process_available_links_failed(self, mock_response):
        mock_response.side_effect = mock.Mock(side_effect=Exception('Error'))  # noqa
        process_available_links(1)

        website_db = Website.query.filter(Website.id == 1).first()  # noqa
        self.assertEqual(Website.query.count(), 1)
        self.assertEqual(website_db.status.value, 'ERROR')
        self.assertEqual(website_db.status_desc, 'Error')  # noqa
        self.assertEqual(mock_response.call_count, 1)

    @mock.patch('pxa.backends.website.WebsiteBackend.save_website_available_links')  # noqa
    def test_website_processing(self, mock_response):
        website = Website()
        website.url = "http://ibm.com.br"
        website.status = Website.Status.NEW
        db.session.add(website)
        db.session.commit()

        website_processing()
        website_db = Website.query.filter(Website.url == website.url).first()  # noqa
        self.assertEqual(website_db.status.value, "PROCESSING")
        self.assertEqual(Website.query.count(), 2)

    def test_website_processing_without_list(self):
        website_db = Website.query.first()  # noqa
        db.session.delete(website_db)
        db.session.commit()
        result = website_processing()
        self.assertEqual(result, None)

    @freeze_time('2018-09-14 15:00:00')
    def test_retry_process_available_links_processing(self):
        website_db = Website.query.first()  # noqa
        db.session.delete(website_db)
        db.session.commit()

        website = Website()
        website.url = "http://ibm.com.br"
        website.status = Website.Status.PROCESSING
        website.updated_dt = datetime(2018, 9, 13, 14, 0)
        db.session.add(website)
        db.session.commit()

        retry_process_available_links_processing()

        website_db = Website.query.first()  # noqa
        self.assertEqual(website_db.status.value, "NEW")

    def test_retry_process_available_links_processing_without_list(self):
        result = retry_process_available_links_processing()
        self.assertEqual(result, None)
