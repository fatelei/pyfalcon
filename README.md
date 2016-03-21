# pyfalcon
Python client for open falcon.

![Build Status](https://travis-ci.org/fatelei/pyfalcon.svg)

# Install

```
pip install pyfalcon
```

# Usage

```
from pyfalcon.client import Client

cli = Client(host="localhost",
             port=1988,
             timeout=1)
cli.gauge("onlineusers", step=60, tags={"loc": "chengdu"})
```

# APIs

## gauge

Using the `gauge` counter type, which means record the value at that time.

### Parameters

+ param str metric: The name of metric
+ param int value: Current value
+ param int step: The cycle of report, default is 60s, optional
+ param dict tags: Tags, optional

### Usage

```
cli.gauge("cpu.idle", 1, tags={"loc": "chengdu"})
```

## timer

Record the cost of time of a function.

### Parameters

+ param str metric: The name of metric, required
+ param int count: Calculate step, default is 1, optional
+ param int step: The cycle of report, default is 60s, optional
+ param dict tags: Tags, optional

### Usage

```
@cli.timer("foo")
def foo():
     print "foo"
```

or

```
def foo():
    print "foo"

with cli.timer("foo"):
     foo()
```
