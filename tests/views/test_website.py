import json

import mock
from elasticsearch.exceptions import ElasticsearchException
from sqlalchemy.exc import SQLAlchemyError

from pxa import db
from pxa.models.no_sql.website import WebsiteNoSql
from pxa.models.website import Website
from tests.base import BaseTestCase


class TestViewWebsite(BaseTestCase):

    def setUp(self):
        self.api_key = 'PXaLogin apikey="test.DU4jJQ.o8vOA378DsITlFQx1etXqt3c-8Q"'  # noqa
        super(TestViewWebsite, self).setUp()
        self.app.test_request_context().push()

    def test_create_website(self):
        params = {
            "url": "http://vtrmantovani.com.br",
        }
        response = self.client.post("/api/website", headers={
            'Authorization': self.api_key,
            'Content-Type': 'application/json'
        }, data=json.dumps(params))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Website.query.count(), 1)

    @mock.patch('pxa.db.session.add')
    def test_create_website_with_sqlalchemy_error(self, mock_db):
        mock_db.side_effect = mock.Mock(side_effect=SQLAlchemyError())
        params = {
            "url": "http://vtrmantovani.com.br",
        }
        response = self.client.post("/api/website", headers={
            'Authorization': self.api_key,
            'Content-Type': 'application/json'
        }, data=json.dumps(params))
        r = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(r['error']['message'], "Some problems in bd")

    def test_get_website(self):
        webiste_nosql = WebsiteNoSql()
        body = {
            'urls': ['http://ibm.com.br']
        }
        webiste_nosql.create(1, body)
        response = self.client.get(
            '/api/website/1',
            headers={'Authorization': 'PXaLogin apikey="xpo"'}
        )
        r = json.loads(response.data.decode('utf-8'))
        self.assertEquals(r['urls'][0], 'http://ibm.com.br')
        self.assertEqual(response.status_code, 200)
        webiste_nosql.delete(1)

    def test_get_website_notfound(self):
        response = self.client.get(
            '/api/website/562',
            headers={'Authorization': 'PXaLogin apikey="xpo"'}
        )
        r = json.loads(response.data.decode('utf-8'))
        self.assertEqual(r['error']['status'], 404)
        self.assertEqual(r['error']['message'], 'Website id not found')

    @mock.patch('pxa.models.no_sql.website.WebsiteNoSql.get')
    def test_get_website_source_not_found(self, mock_get):
        mock_get.return_value = {'_source': ''}
        response = self.client.get(
            '/api/website/1',
            headers={'Authorization': 'PXaLogin apikey="xpo"'}
        )
        r = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(r['error']['message'], "Source not found")

    @mock.patch('pxa.models.no_sql.website.WebsiteNoSql.get')
    def test_get_website_with_elasticsearch_exception(self, mock_get):
        mock_get.side_effect = mock.Mock(side_effect=ElasticsearchException())
        response = self.client.get(
            '/api/website/1',
            headers={'Authorization': 'PXaLogin apikey="xpo"'}
        )
        r = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(r['error']['message'], "Some problems in bd")

    def test_search_website_with_status_done(self):
        website = Website()
        website.url = "http://vtrmantovani.com.br"
        website.status = Website.Status.DONE
        db.session.add(website)
        db.session.commit()
        self.assertEqual(Website.query.count(), 1)
        webiste_nosql = WebsiteNoSql()
        body = {
            'urls': ['http://ibm.com.br']
        }
        webiste_nosql.create(1, body)

        params = {
          "status": "DONE",
          "limit": 2,
          "offset": 0
        }
        response = self.client.post("/api/search", headers={
            'Authorization': self.api_key,
            'Content-Type': 'application/json'
        }, data=json.dumps(params))
        r = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(r['websites'][0]['website'], "http://vtrmantovani.com.br")  # noqa
        self.assertEqual(r['websites'][0]['urls'][0], "http://ibm.com.br")
        self.assertEqual(r['total_itens'], 1)
        webiste_nosql.delete(1)

    def test_search_website_with_status_done_withot_website_nosql(self):
        website = Website()
        website.url = "http://vtrmantovani.com.br"
        website.status = Website.Status.DONE
        db.session.add(website)
        db.session.commit()
        self.assertEqual(Website.query.count(), 1)
        params = {
          "status": "DONE",
          "limit": 2,
          "offset": 0
        }
        response = self.client.post("/api/search", headers={
            'Authorization': self.api_key,
            'Content-Type': 'application/json'
        }, data=json.dumps(params))
        r = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(r['error']['message'], "Website id not found")

    def test_search_website_without_status_done(self):
        website = Website()
        website.url = 'http://ibm.com.br'
        website.status = Website.Status.NEW
        db.session.add(website)
        db.session.commit()
        self.assertEqual(Website.query.count(), 1)

        params = {
          "status": "NEW",
          "limit": 2,
          "offset": 0
        }
        response = self.client.post("/api/search", headers={
            'Authorization': self.api_key,
            'Content-Type': 'application/json'
        }, data=json.dumps(params))
        r = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(r['websites'][0]['website'], "http://ibm.com.br")
        self.assertEqual(r['total_itens'], 1)

    @mock.patch('pxa.models.no_sql.website.WebsiteNoSql.get')
    def test_search_website_with_elasticsearch_exception(self, mock_get):
        mock_get.side_effect = mock.Mock(side_effect=ElasticsearchException())
        website = Website()
        website.url = "http://vtrmantovani.com.br"
        website.status = Website.Status.DONE
        db.session.add(website)
        db.session.commit()
        self.assertEqual(Website.query.count(), 1)
        params = {
          "status": "DONE",
          "limit": 2,
          "offset": 0
        }
        response = self.client.post("/api/search", headers={
            'Authorization': self.api_key,
            'Content-Type': 'application/json'
        }, data=json.dumps(params))
        r = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(r['error']['message'], "Some problems in bd")
