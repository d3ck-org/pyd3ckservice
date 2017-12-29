#pylint: disable=W0401

try:
    __import__('elasticsearch')
    from .elasticsearch import main as elasticsearch
except ImportError:
    pass

try:
    __import__('pymongo')
    from .mongo import main as mongo
except ImportError:
    pass

try:
    __import__('redis')
    from .redis import main as redis
except ImportError:
    pass

try:
    __import__('flask')
    from .flask import main as flask
except ImportError:
    pass
