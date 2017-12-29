import logging
from flask import request as req, jsonify, abort
from voluptuous import Schema as VoS, Required as VoR
import pyd3ckbase as __
import pyd3ckservice.flask as srv_flask
from main import app_

log = logging.getLogger(__name__)

_mockData = {
    __.to_uuid('a868f0a0-a68c-486f-9104-97ef6368e8af'): {
        '_id': __.to_uuid('a868f0a0-a68c-486f-9104-97ef6368e8af'),
        'model': 'S 1000 RR',
        'brand': 'BMW',
        'category': 1
    },
    __.to_uuid('c4ff0239-f68e-4c3a-8ab9-e3e714536f55'): {
        '_id': __.to_uuid('c4ff0239-f68e-4c3a-8ab9-e3e714536f55'),
        'model': 'F4 RR',
        'brand': 'MV',
        'category': 2
    },
    __.to_uuid('d225a93b-c287-4922-94f2-c95507d82e2f'): {
        '_id': __.to_uuid('d225a93b-c287-4922-94f2-c95507d82e2f'),
        'model': 'Panigale R',
        'brand': 'Ducati',
        'category': 2
    },
}


def _get_mock(d=None):
    return _mockData.get(
        d) if d else [_mockData[_id] for _id in sorted(_mockData)]


def _set_mock(d, rm=False):
    if rm:
        del _mockData[d]
    else:
        _mockData[d['_id']] = d


@app_.route('/bikes/<uuid:_id>')
def show(_id):
    log.debug('Getting bike %s', _id)
    return jsonify(_get_mock(_id) or abort(404))


@app_.route('/bikes/<uuid:_id>', methods=['DELETE'])
def remove(_id):
    log.debug('Deleting bike %s', _id)
    try:
        _set_mock(_id, True)
    except KeyError:
        abort(404)
    return jsonify(srv_flask.get_result())


@app_.route('/bikes')
@app_.route('/bikes/<int:limit>')
def find(limit=None):
    log.debug('Gettings all bikes')
    vos = VoS({'brand': str, 'category': srv_flask.to_int})
    fltr = vos(req.args)
    rsrcs = _get_mock()
    for key in ['brand', 'category']:
        if key in fltr:
            rsrcs = [it for it in rsrcs if fltr[key] == it[key]]
    return jsonify(rsrcs[:limit])


@app_.route('/bikes', methods=['POST'])
def create():
    vos = VoS({VoR('model'): str, VoR('brand'): str})
    rsrc = vos(req.get_json(force=True))
    rsrc.update({'_id': __.get_uuid()})
    log.debug('Creating bike %s (%s)', rsrc['_id'], rsrc['model'])
    _set_mock(rsrc)
    return jsonify(rsrc)


@app_.route('/bikes', methods=['PUT'])
def edit():
    vos = VoS({VoR('_id'): __.to_uuid, 'model': str, 'brand': str})
    irsrc = vos(req.get_json(force=True))
    log.debug('Getting bike %s', irsrc['_id'])
    rsrc = _get_mock(irsrc['_id']) or abort(404)
    log.debug('Updating bike %s (%s)', rsrc['_id'], rsrc['model'])
    rsrc.update(irsrc)
    _set_mock(rsrc)
    return jsonify(rsrc)
