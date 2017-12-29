from os import chdir as os_chdir
from pathlib import Path
os_chdir(Path(__file__).resolve().parent)
from sys import path as sys_path
sys_path.append('lib')
import logging
import pyd3ckbase as __
import pyd3ckservice.mongo as srv_mongo

try:
    _cfg = __.init(__.get_arg_parser())
    log = logging.getLogger(__name__)
except __.Err as _e:
    __.die(_e)

_cfg['mongo'] = {
    'uri': 'mongodb://127.0.0.1:27017',
    'cfg': {
        'serverSelectionTimeoutMS': 30000
    }
}

try:
    log.info('Initializing mongo')
    _mgc = srv_mongo.init(_cfg['mongo']['uri'], _cfg['mongo']['cfg'])
    log.info('Connection to %s successfully tested', _cfg['mongo']['uri'])
except AttributeError:
    __.die('Please install pymongo with "pip install pymongo"')
except __.Err as _e:
    __.die(_e)
