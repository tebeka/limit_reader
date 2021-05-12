# LimitReader - Wrap readers with a limit

A port of Go's [io.LimitReader](https://golang.org/pkg/io/#LimitReader) to Python.


### Example

```python
>>> from io import StringIO
>>> rdr = LimitReader(StringIO('abcdef'), 3)
>>> rdr.read()
'abc'
>>> rdr.close()  # close is proxied to the embedded reader
```
