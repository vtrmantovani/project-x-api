import requests
from bs4 import BeautifulSoup
from flask import current_app as app
from requests.exceptions import ConnectionError

from pxa import db, logger
from pxa.backends.exceptions import WebsiteBackendException
from pxa.models.no_sql.website import WebsiteNoSql
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

    def _check_if_website_exist_done(self, url):
        website = Website.query.filter(Website.url==url).filter(Website.status == Website.Status.DONE).first()  # noqa
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
                if is_valid_url(url_website):
                    list_urls.append(url_website)

        return list_urls

    def _put_website_links_on_quee(self, list_urls):
        for url_website in list_urls:
            if is_valid_url(url_website):
                self._save_website(url_website)

    def _save_website_links(self, website, list_urls):
        website_nosql = WebsiteNoSql()
        body = {
            'urls': list_urls
        }

        check_website_exist_done = self._check_if_website_exist_done(website.url) # noqa

        if check_website_exist_done is False:
            self._put_website_links_on_quee(list_urls)
            website_nosql.create(website.id, body)
        else:
            website_done = Website.query\
                .filter(Website.url == website.url)\
                .filter(Website.status == Website.Status.DONE).first()
            website_nosql_db = website_nosql.get(website_done.id)
            if website_nosql_db:
                if website_nosql_db['_source'] != body:
                    self._put_website_links_on_quee(list_urls)
                    website_nosql.create(website.id, body)
                    website_nosql.update(website_done.id, body)
                else:
                    website_nosql.create(website.id, body)
            else:
                logger.error("Website NoSql not found: on website_id {0}".format(website_done.id) ) # noqa
                raise WebsiteBackendException("Website NoSql not found")

    def save_website_available_links(self, website):

        list_urls = self._get_available_links(website)
        self._save_website_links(website, list_urls)

        website_db = Website.query.filter(Website.id == website.id).first()
        website_db.status = Website.Status.DONE
        db.session.add(website_db)
        db.session.commit()
