import configparser, os, logging

from application.common.path_utils import PathUtils
from elasticsearch import Elasticsearch

logging.basicConfig(level=logging.INFO)
g_root_path = os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
g_config = configparser.ConfigParser()
g_pathUtils = PathUtils(os.path.dirname(__file__))

class EsHelper:
    def __init__(self):
        config_path = os.path.join(g_pathUtils.find_resource_dir(), 'config.ini')
        g_config.read(config_path)

        # ES properties
        es_host = g_config['elasticsearch']['host']
        es_port = g_config['elasticsearch']['port']
        es_user_name = g_config['elasticsearch']['user_name']
        es_password = g_config['elasticsearch']['password']
        es_use_ssl = g_config.getboolean('elasticsearch', 'use_ssl')
        es_ssl_certificate_check = g_config.getboolean('elasticsearch', 'ssl_certificate_check')
        es_ssl_cert = g_config['elasticsearch']['ssl_cert']

        es_url = ('https://' if es_use_ssl else 'http://') + es_host + ':' + es_port

        # ES Helper
        if es_use_ssl:
            self.es = Elasticsearch(hosts=es_url, basic_auth=(es_user_name, es_password), verify_certs=es_ssl_certificate_check, ssl_context=es_ssl_cert)
        else:
            self.es = Elasticsearch(hosts=es_url, basic_auth=(es_user_name, es_password), verify_certs=False)

    def get_cluster_health(self):
        return self.es.cluster.health()
    def get_analyzed_token(self, analyzer, text, index_name=None):
        response = self.es.indices.analyze(
            index=index_name,
            body={
                "analyzer": analyzer,
                "text": text
            }
        )
        tokens = [item['token'] for item in response['tokens']]
        return tokens


if __name__ == '__main__':
    es_helper = EsHelper()
    print(es_helper.get_cluster_health())
    print(es_helper.get_analyzed_token(analyzer="nori", text="부의추월차선"))
    print(es_helper.get_analyzed_token(index_name="book-test", analyzer="nori", text="부의추월차선"))