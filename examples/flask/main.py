from os import chdir as os_chdir
from pathlib import Path
os_chdir(Path(__file__).resolve().parent)
from sys import path as sys_path
sys_path.append('lib')
import logging
from flask import Flask
import pyd3ckbase as __
import pyd3ckservice.flask as srv_flask

try:
    # don't use arg_parser: doesn't work with "flask" binary
    _cfg = __.init(_fpath=Path(__file__).resolve())
    log = logging.getLogger(__name__)
except __.Err as _e:
    __.die(_e)

_cfg['flask'] = {
    # http://flask.pocoo.org/docs/latest/config/#builtin-configuration-values
    'cfg': {
        'JSONIFY_PRETTYPRINT_REGULAR': True,
        'JSON_SORT_KEYS': True,
        # http://stackoverflow.com/a/36379452
        'JSON_AS_ASCII': False
    }
}

log.info('Initializing flask')
app_ = Flask(__name__)
try:
    srv_flask.init(_cfg['flask'], app_, srv_flask.json_error_handler)
except AttributeError:
    __.die('Please install flask with "pip install Flask"')
except __.Err as _e:
    __.die(_e)

# @app_.before_request
# def before_request():
#     ...

# @app_.teardown_request
# def teardown_request(exception):
#     ...

import api  #pylint: disable=W0611
