# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import logging

from numbers import Number
from collections import Set, Mapping, deque
from datetime import datetime

zero_depth_bases = (str, bytes, Number, range, bytearray)
iteritems = 'items'


def getsize(obj_0):
    """Recursively iterate to sum size of object and members

    By Aaron Hall
    https://stackoverflow.com/questions/449560/how-do-i-determine-the-size-of-an-object-in-python
    """
    _seen_ids = set()

    def inner(obj):
        obj_id = id(obj)
        if obj_id in _seen_ids:
            return 0
        _seen_ids.add(obj_id)
        size = sys.getsizeof(obj)
        if isinstance(obj, zero_depth_bases):
            pass  # bypass remaining control flow and return
        elif isinstance(obj, (tuple, list, Set, deque)):
            size += sum(inner(i) for i in obj)
        elif isinstance(obj, Mapping) or hasattr(obj, iteritems):
            size += sum(inner(k) + inner(v)
                        for k, v in getattr(obj, iteritems)())
        # Check for custom object instances - may subclass above too
        if hasattr(obj, '__dict__'):
            size += inner(vars(obj))
        if hasattr(obj, '__slots__'):  # can have __slots__ with __dict__
            size += sum(inner(getattr(obj, s))
                        for s in obj.__slots__ if hasattr(obj, s))
        return size
    return inner(obj_0)


def _time_elapsed(start):
    """
    """
    return (datetime.now() - start).total_seconds()


def get_logger():
    """
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.INFO)
    streamFormatter = logging.Formatter('[%(levelname)s] %(message)s')
    streamHandler.setFormatter(streamFormatter)
    logger.addHandler(streamHandler)
    return logger

from pymerkle import MerkleTree

def tree_benchmark():
    t = MerkleTree()
    print(getsize(t))
    start = datetime.now()
    for i in range(100000):
        t.encryptRecord('%d-th record' % i)
    print(_time_elapsed(start))
    print(getsize(t))


if __name__ == "__main__":
    tree_benchmark()
    sys.exit(0)