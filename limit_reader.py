__version__ = '0.1.0'


class LimitReader:
    """LimitReader wraps a "reader" object (has a "read" method)

    LimitReader will limit called to "read" up to "limit". It'll proxy all
    other attributes to the original object.

    >>> from io import StringIO
    >>> rdr = LimitReader(StringIO('abcdef'), 3)
    >>> rdr.read()
    'abc'
    >>> rdr.close()  # close is proxied to the embedded reader
    """
    def __init__(self, obj, limit, sentinel=b''):
        self.__obj = obj
        self.__limit = limit
        self.__size = 0
        self.__sentinel = sentinel

    def __repr__(self):
        return repr(self.__obj)

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
