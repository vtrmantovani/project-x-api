import requests
from bs4 import BeautifulSoup
from flask import current_app as app
from requests.exceptions import ConnectionError, ConnectTimeout

from pxa import logger
from pxa.backends.exceptions import WebsiteBackendException
from pxa.utils.validators import is_valid_url


class WebsiteBackend:

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

        except ConnectTimeout as e:
            logger.warning("ConnectTimeout on website {0} - {1}".format(url, str(e)))  # noqa
            raise ConnectTimeout()
        except ConnectionError as e:
            logger.error("ConnectionError: on website {0} - {1}".format(url, str(e)))  # noqa
            raise WebsiteBackendException("ConnectionError on request")

    def get_available_links(self, website):

        list_urls = []

        html = self._get_response_website(website)

        search_websites_response = BeautifulSoup(html, 'lxml')\
            .find_all('a', href=True)

        if search_websites_response:
            for url_website in search_websites_response:
                url_website = url_website['href']
                if is_valid_url(url_website):
                    list_urls.append(url_website)

        return list_urls
