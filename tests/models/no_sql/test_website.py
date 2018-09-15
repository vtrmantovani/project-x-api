import mock
from elasticsearch.exceptions import ElasticsearchException

from pxa.models.no_sql.website import WebsiteNoSql
from tests.base import BaseTestCase


class TestModelNoSqlWebsite(BaseTestCase):

    def test_create_website_document(self):
        webiste_nosql = WebsiteNoSql()
        body = {
            'urls': ['http://ibm.com.br']
        }
        webiste_nosql.create(2, body)
        webiste_nosql.delete(2)

    @mock.patch('pxa.models.no_sql.website.es.index')
    def test_create_website_document_with_error(self, mock_elastich):
        mock_elastich.side_effect = mock.Mock(side_effect=ElasticsearchException())  # noqa
        with self.assertRaises(ElasticsearchException):
            webiste_nosql = WebsiteNoSql()
            body = {
                'urls': ['http://ibm.com.br']
            }

            webiste_nosql.create(12, body)
        self.assertEqual(mock_elastich.call_count, 1)

    def test_get_website_document(self):
        webiste_nosql = WebsiteNoSql()
        body = {
            'urls': ['http://ibm.com.br']
        }
        webiste_nosql.create(3, body)

        bd_web_site = webiste_nosql.get(3)
        body = {
            'urls': ['http://ibm.com.br']
        }
        self.assertEquals(bd_web_site['_source'], body)
        webiste_nosql.delete(3)

    def test_get_website_document_not_found(self):
        webiste_nosql = WebsiteNoSql()
        bd_web_site = webiste_nosql.get(1)
        self.assertEquals(bd_web_site, None)

    @mock.patch('pxa.models.no_sql.website.es.get')  # noqa
    def test_get_website_document_with_error(self, mock_elastich):
        mock_elastich.side_effect = mock.Mock(side_effect=ElasticsearchException())  # noqa
        with self.assertRaises(ElasticsearchException):
            webiste_nosql = WebsiteNoSql()
            webiste_nosql.get(1)
        self.assertEqual(mock_elastich.call_count, 1)

    def test_update_website_document(self):
        webiste_nosql = WebsiteNoSql()
        body = {
            'urls': ['http://ibm.com.br']
        }
        webiste_nosql.create(4, body)

        body = {
            'urls': ['http://vtrmantovani.com.br']
        }
        webiste_nosql.update(4, body)
        bd_web_site = webiste_nosql.get(4)
        self.assertEquals(bd_web_site['_source'], body)
        webiste_nosql.delete(4)

    @mock.patch('pxa.models.no_sql.website.es.update')  # noqa
    def test_update_website_document_with_error(self, mock_elastich):
        mock_elastich.side_effect = mock.Mock(side_effect=ElasticsearchException())  # noqa
        with self.assertRaises(ElasticsearchException):
            body = {
                'urls': ['http://vtrmantovani.com.br']
            }
            webiste_nosql = WebsiteNoSql()
            webiste_nosql.update(1, body)
        self.assertEqual(mock_elastich.call_count, 1)

    def test_delete_website_document(self):
        webiste_nosql = WebsiteNoSql()
        body = {
            'urls': ['http://ibm.com.br']
        }
        webiste_nosql.create(2, body)

        webiste_nosql = WebsiteNoSql()
        webiste_nosql.delete(2)

    @mock.patch('pxa.models.no_sql.website.es.delete')  # noqa
    def test_delete_website_document_with_error(self, mock_elastich):
        mock_elastich.side_effect = mock.Mock(side_effect=ElasticsearchException())  # noqa
        with self.assertRaises(ElasticsearchException):
            webiste_nosql = WebsiteNoSql()
            webiste_nosql.delete(1)

        self.assertEqual(mock_elastich.call_count, 1)
