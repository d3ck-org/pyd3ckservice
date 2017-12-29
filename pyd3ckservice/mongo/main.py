import logging
from pymongo import MongoClient as PyMongoClient
from pymongo.errors import PyMongoError
import pyd3ckbase as __

log = logging.getLogger(__name__)


def init(uri, cfg):
    if not 'connTest' in cfg:
        cfg['connTest'] = True
    return get_client(uri, cfg)


def get_client(uri, cfg):
    try:
        if cfg.get('connTest'):
            del cfg['connTest']
            # check connection: http://stackoverflow.com/a/30539401
            mgc = PyMongoClient(uri, serverSelectionTimeoutMS=1)
            mgc.database_names()  # check connection
        mgc = PyMongoClient(uri, **cfg)
        log.debug('Connected to %s', uri)
    except PyMongoError as e:
        raise __.DataErr('Connecting to {} failed: {}'.format(uri, e))
    return mgc
