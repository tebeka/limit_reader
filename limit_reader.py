"""Wrap an object to limit the amount of data read."""
__version__ = '0.1.0'


class LimitReader:
    """LimitReader wraps a "reader" object (has a "read" method)

    LimitReader will limit called to "read" up to "limit". It'll proxy all
    other attributes to the original object.

    Parameters
    ----------
    obj: object
        Object to wrap, it should have a "read" method
    limit: int
        Read size limit in bytes
    sentinel: object
        Value to return after reaching limit

    >>> from io import StringIO
    >>> rdr = LimitReader(StringIO('abcdef'), 3)
    >>> rdr.read()
    'abc'
    >>> rdr.close()  # close is proxied to the embedded reader
    """
    def __init__(self, obj, limit, sentinel=b''):
        fn = getattr(obj, 'read', None)
        if not callable(fn):
            raise TypeError(f'{obj!r} has not "read" method')

        self.__obj = obj
        self.__limit = limit
        self.__size = 0
        self.__sentinel = sentinel

    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls}({self.__obj!r}, {self.__limit}, ' + \
               f'sentinel={self.__sentinel!r}'

    def __getattr__(self, attr):
        return getattr(self.__obj, attr)

    def read(self, size=None):
        if self.__size == self.__limit:
            return self.__sentinel

        if size is None:
            size = self.__limit

        size = min(self.__limit - self.__size, size)
        data = self.__obj.read(size)
        self.__size += size
        return data

    def unwrap(self):
        """Returns the original object"""
        return self.__obj

    def dir(self):
        return sorted(dir(self.__obj) + ['unwrap'])
