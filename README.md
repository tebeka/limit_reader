# LimitReader - Wrap readers with a limit

A port of Go's [io.LimitReader](https://golang.org/pkg/io/#LimitReader) to Python.

**THIS CODE IS STILL IN ALPHA PHASE, USE AT YOUR OWN RISK**


### Examples

#### HTTP Requests

```python
>>> from urllib.request import urlopen
>>> from limit_reader import LimitReader
>>> with urlopen('https://httpbin.org/bytes/1000') as resp:
...     rdr = LimitReader(resp, 353)
...     print(rdr.status)  # proxies method
...     data = rdr.read()
... 
200
>>> print(len(data))
353
```

#### Files

```python
>>> with open('README.md') as fp:
...     rdr = LimitReader(fp, 17)
...     print(rdr.name)
...     data = rdr.read()
... 
README.md
>>> print(len(data))
17
```
