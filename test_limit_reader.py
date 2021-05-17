import re
import sys
from io import BytesIO
from pathlib import Path
from random import randbytes
from subprocess import PIPE, Popen
from urllib.request import urlopen
from http import HTTPStatus

import pytest

from limit_reader import LimitReader


def new_reader(size, limit):
    data = randbytes(size)
    io = BytesIO(data)

    return data, LimitReader(io, limit)


test_cases = [
    # n, limit, read_size
    (117, 118, None),
    (73, 70, None),
    (37, 37, None),
    (100, 10, 3),
    (100, 10, 32),
    (100, 0, 32),
    (100, 100, 0),
]


@pytest.mark.parametrize('n, limit, read_size', test_cases)
def test_limit(n, limit, read_size):
    data = randbytes(n)
    io = BytesIO(data)
    rdr = LimitReader(io, limit)
    out = rdr.read(read_size)
    if read_size is None:
        end = limit
    else:
        end = min(limit, read_size)
    assert out == data[:end]


def test_attrs():
    io = BytesIO()
    rdr = LimitReader(io, 100)
    rdr.close()  # show now raise

    with pytest.raises(AttributeError):
        rdr.no_such_method


def test_validate():
    with pytest.raises(TypeError):
        LimitReader('oops')


def test_request(httpd_port):
    readme = Path('README.md')
    file_size = readme.stat().st_size

    resp = urlopen(f'http://localhost:{httpd_port}/{readme.name}')
    read_size = file_size - 42
    r = LimitReader(resp, read_size)
    assert r.status == HTTPStatus.OK
    data = r.read()
    assert read_size == len(data)


def test_file():
    readme = Path('README.md')
    file_size = readme.stat().st_size
    read_size = file_size - 7
    with readme.open() as fp:
        r = LimitReader(fp, read_size)
        assert r.name == readme.name
        data = r.read()
    assert read_size == len(data)


@pytest.fixture
def httpd_port():
    # -u for unbuffered stdout, port 0 will pick random free port
    p = Popen([sys.executable, '-u', '-m', 'http.server', '0'], stdout=PIPE)
    line = p.stdout.readline().decode()
    # Serving HTTP on 0.0.0.0 port 42441 (http://0.0.0.0:42441/) ...
    match = re.search(r'port (\d+)', line)
    assert match, 'cannot find port in: {line!r}'
    port = int(match.group(1))

    yield port

    p.kill()
