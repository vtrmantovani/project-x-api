import requests
from bs4 import BeautifulSoup
from flask import current_app as app
from requests.exceptions import ConnectionError

from pxa import db, logger
from pxa.backends.exceptions import WebsiteBackendException
from pxa.models.website import Website
from pxa.utils.validators import is_valid_url


class WebsiteBackend:

    def _save_website(self, url):
        website = Website()
        website.url = url
        website.status = Website.Status.NEW
        db.session.add(website)
        db.session.commit()

    def failed_save_website_available_links(self, website, desc):
        website.status = Website.Status.ERROR
        website.status_desc = desc
        db.session.add(website)
        db.session.commit()

    def _check_if_website_exist(self, url):
        website = Website.query.filter(Website.url == url).first()  # noqa
        if website:
            return True

        return False

    def _get_response_website(self, website):
        try:
            url = website.url
            response = requests.get(url, timeout=app.config['TIMEOUT_WEBSITE'])

            if response.status_code != 200:
                logger.error("Response status code not is 200: {0}".format(url))  # noqa
                raise WebsiteBackendException("Response status code not is 200")  # noqa

            if not response.text:
                logger.error("Response text without value: {0}".format(url))  # noqa
                raise WebsiteBackendException("Response text without value")

            return response.text

        except ConnectionError as e:
            logger.error("ConnectionError: on website {0} - {1}".format(url, str(e)))  # noqa
            raise WebsiteBackendException("ConnectionError on request")

    def _get_available_links(self, website):

        list_urls = []

        html = self._get_response_website(website)

        search_websites_response = BeautifulSoup(html, 'lxml')\
            .find_all('a', href=True)

        if search_websites_response:
            for url_website in search_websites_response:
                url_website = url_website['href']
                if is_valid_url(url_website) and self._check_if_website_exist(url_website) is False:  # noqa
                    self._save_website(url_website)
                    list_urls.append(url_website)

        return list_urls

    def save_website_available_links(self, website):

        self._get_available_links(website)

        website_db = Website.query.filter(Website.id == website.id).first()
        website_db.status = Website.Status.DONE
        db.session.add(website_db)
        db.session.commit()
