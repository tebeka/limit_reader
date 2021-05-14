from io import BytesIO
from random import randbytes

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
