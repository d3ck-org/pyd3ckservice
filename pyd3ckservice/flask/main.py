import logging
from werkzeug.exceptions import default_exceptions as werkzeug_default_exceptions, InternalServerError as werkzeug_InternalServerError
from flask import jsonify as flask_jsonify
from voluptuous.error import Error as VoErr, MultipleInvalid as VoMultErr
import pyd3ckbase as __

log = logging.getLogger(__name__)


def init(cfg, app, error_handler=None):
    # http://flask.pocoo.org/docs/latest/config/#builtin-configuration-values
    app.config.update(**cfg['cfg'])

    # http://werkzeug.pocoo.org/docs/latest/exceptions/
    # https://github.com/pallets/flask/issues/941#issuecomment-31686642
    # https://github.com/pallets/flask/issues/941#issuecomment-118975275
    # http://flask.pocoo.org/docs/latest/config/#builtin-configuration-values
    # http://stackoverflow.com/a/33711404
    # http://stackoverflow.com/a/36575875

    # app.config['TRAP_HTTP_EXCEPTIONS'] = True
    if not error_handler:
        error_handler = json_error_handler
    for e in werkzeug_default_exceptions.items():
        app.register_error_handler(e[1], error_handler)
    app.register_error_handler(VoErr, error_handler)
    app.register_error_handler(__.Err, error_handler)


def json_error_handler(e, msg404='Not found: Please check URL and/or ID'):
    if isinstance(e, VoErr):
        code = 400
        msg = 'Invalid data'
        if isinstance(e, VoMultErr):
            msg += ': ' + '; '.join([str(e_) for e_ in e.errors])
        else:
            msg += str(e) or ''
        log.debug('Request aborted: %s: %s', code, msg)
    else:
        msg = getattr(e, 'message', getattr(e, 'description', 'Unknown error'))
        code = int(getattr(e, 'code', 500))
        code = code or 500
        msg = msg404 if code == 404 and msg404 else msg
        if code >= 400 and code < 500:
            log.debug('Request aborted: %s: %s', code, msg)
        else:
            log.error('Request aborted: %s: %s', code, msg)
        if code >= 500:
            msg = werkzeug_InternalServerError.description
    try:
        return flask_jsonify({'code': code, 'msg': msg}), code
    except (ValueError, KeyError, TypeError):
        raise e.get_response()


def get_result(sts='ok'):
    return {'result': sts}


def to_int(value):
    # helper for voluptuous:
    #   https://julien.danjou.info/blog/2015/python-schema-validation-voluptuous
    #     It's not possible to use directly 'int' in the schema, otherwise
    #     Voluptuous would check that the data is actually an instance of int.
    return int(value)


def to_float(value):
    # helper for voluptuous
    return float(value)


def to_bool(value):
    # helper for voluptuous
    value = str(value).lower()
    if value in ['true', '1']:
        return True
    elif value in ['false', '0']:
        return False
    else:
        raise ValueError('{} is not a boolean expression'.format(value))
