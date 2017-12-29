from os import chdir as os_chdir
from pathlib import Path
os_chdir(Path(__file__).resolve().parent)
from sys import path as sys_path
sys_path.append('lib')
import logging
import pyd3ckbase as __
import pyd3ckservice.redis as srv_redis

try:
    _cfg = __.init(__.get_arg_parser())
    log = logging.getLogger(__name__)
except __.Err as _e:
    __.die(_e)

_cfg['redis'] = {
    # https://redis-py.readthedocs.io/en/latest/index.html#redis.StrictRedis.from_url
    'uri': 'redis://127.0.0.1:6379',
    'cfg': {
        # 'encoding': 'utf-8'    # default is utf-8
    }
}

try:
    log.info('Initializing redis')
    _mgc = srv_redis.init(_cfg['redis']['uri'], _cfg['redis']['cfg'])
    log.info('Connection to %s successfully tested', _cfg['redis']['uri'])
except AttributeError:
    __.die('Please install redis-py with "pip install redis"')
except __.Err as _e:
    __.die(_e)
