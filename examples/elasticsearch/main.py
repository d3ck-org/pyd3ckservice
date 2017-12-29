from os import chdir as os_chdir
from pathlib import Path
os_chdir(Path(__file__).resolve().parent)
from sys import path as sys_path
sys_path.append('lib')
import logging
import pyd3ckbase as __
import pyd3ckservice.elasticsearch as srv_es

try:
    _cfg = __.init(__.get_arg_parser())
    log = logging.getLogger(__name__)
except __.Err as _e:
    __.die(_e)

_cfg.update({
    'es': {
        # 'urls': ['http://127.0.0.1:9200', 'http://127.0.0.2:9200'],
        'url': 'http://127.0.0.1:9200',
        'cfg': {
            'timeout': 10
        }
    },
    '_moduleLogLevel': 'WARN'  # but '-v' overwrites this setting
})

try:
    log.info('Initializing elasticsearch')
    # _es = srv_es.init(_cfg['es']['urls'], _cfg['es']['cfg'])
    _es = srv_es.init(_cfg['es']['url'], _cfg['es']['cfg'])
    logging.getLogger('elasticsearch').setLevel(_cfg['_moduleLogLevel'])
    log.info('Connection to %s successfully tested', _cfg['es']['url'])
except AttributeError as e:
    __.die('Please install elasticsearch with "pip install elasticsearch"')
except __.Err as _e:
    __.die(_e)
