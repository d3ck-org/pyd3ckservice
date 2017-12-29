import logging
from redis import StrictRedis as StrictRedis
from redis.exceptions import RedisError
import pyd3ckbase as __

log = logging.getLogger(__name__)


def init(uri, cfg):
    if not 'connTest' in cfg:
        cfg['connTest'] = True
    if not 'decode_responses' in cfg:
        cfg['decode_responses'] = True
    if not 'encoding' in cfg:
        cfg['encoding'] = 'utf-8'
    return get_client(uri, cfg)


def get_client(uri, cfg):
    try:
        if cfg.get('connTest'):
            del cfg['connTest']
            # check connection
            rdc = StrictRedis.from_url(
                uri, socket_connect_timeout=1)  # seconds?
            rdc.ping()
        # StrictRedis() vs. Redis():
        #   http://stackoverflow.com/a/19024045
        # StrictRedis.from_url():
        #   https://redis-py.readthedocs.io/en/latest/index.html#redis.StrictRedis.from_url
        rdc = StrictRedis.from_url(uri, **cfg)
        log.debug('Connected to %s', uri)
    except RedisError as e:
        raise __.DataErr('Connecting to {} failed: {}'.format(uri, e))
    return rdc
