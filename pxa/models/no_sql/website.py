from elasticsearch.exceptions import ElasticsearchException, NotFoundError

from pxa import es, logger


class WebsiteNoSql:

    def create(self, id_webiste, body):
        try:
            es.index(
                index="website",
                doc_type='website-type',
                id=id_webiste,
                body=body
            )
        except ElasticsearchException as e:
            logger.exception("WebsiteNoSql create. website_id={0}, body={1}, Erro:{1}".format(id_webiste, str(body), str(e)))  # noqa
            raise ElasticsearchException()

    def get(self, id_webiste):
        try:
            return es.get(
                index="website",
                doc_type='website-type',
                id=id_webiste
            )
        except NotFoundError as e:
            return None
        except ElasticsearchException as e:
            logger.exception("WebsiteNoSql get. website_id={0}.  Erro:{1}".format(id_webiste, str(e)))  # noqa
            raise ElasticsearchException()

    def update(self, id_webiste, body):
        try:
            es.update(
                index="website",
                doc_type='website-type',
                id=id_webiste,
                body={"doc": body}
            )
        except ElasticsearchException as e:
            logger.exception("WebsiteNoSql update. website_id={0}, body={1}, Erro:{1}".format(id_webiste, str(body), str(e)))  # noqa
            raise ElasticsearchException()

    def delete(self, id_webiste):
        try:
            return es.delete(
                index="website",
                doc_type='website-type',
                id=id_webiste
            )
        except ElasticsearchException as e:
            logger.exception("WebsiteNoSql delete. website_id={0}.  Erro:{1}".format(id_webiste, str(e)))  # noqa
            raise ElasticsearchException()
