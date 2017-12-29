import logging
from elasticsearch import Elasticsearch, ElasticsearchException, ImproperlyConfigured
import pyd3ckbase as __

log = logging.getLogger(__name__)


def init(urls, cfg):
    if not 'connTest' in cfg:
        cfg['connTest'] = True
    return get_client(urls, cfg)


def get_client(urls, cfg):
    label = 'elasticsearch-nodes ' + ','.join(urls) if isinstance(
        urls, list) else 'elasticsearch-node ' + urls
    try:
        if cfg.get('connTest'):
            del cfg['connTest']
            es = Elasticsearch(urls, **cfg)
            es.info()  # check connection
        else:
            es = Elasticsearch(urls, **cfg)
        log.debug('Connected to %s', label)
    except (ElasticsearchException, ImproperlyConfigured) as e:
        raise __.DataErr('Connecting to {} failed: {}'.format(label, e))
    return es
