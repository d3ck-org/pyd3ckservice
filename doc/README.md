# pyd3ckservice

Test project, don't use in production.

## Requirements

- Python version >= 3.4
- Python modules (optional):
  - `pyd3ckservice` only loads a service when it is possible to import the underlying module.
  - Before installation: (Don't) comment services in the following `requirements.txt` and run `pip install -r requirements.txt`.

```shell
$ cat requirements.txt

# mongo
pymongo >= 3.4.0

# flask
Flask >= 0.12

# redis
#   https://github.com/andymccurdy/redis-py#parsers
redis >= 2.10.5
hiredis >= 0.2.0

# elasticsearch
#   mandatory for elasticsearch module: set the matching major version
#     https://elasticsearch-py.readthedocs.io/en/master/index.html
elasticsearch >= 5.0.0, < 6.0.0
```

## Installation

```shell
$ pip install -r requirements.txt   # see above
$ pip install --process-dependency-links git+https://github.com/d3ck-org/pyd3ckservice.git
```

