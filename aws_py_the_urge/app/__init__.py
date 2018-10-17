"""aws_py_the_urge - An opinionated, minimal cookiecutter template for Python packages"""

__version__ = '0.1.0'
__author__ = 'the urge <pierre.caserta@gmail.com>'
__all__ = []

import urllib.parse
from typing import NamedTuple, Text

EventRecordBase = NamedTuple("EventRecordBase",
                             [("object_key", Text), ("event_name", Text),
                              ("bucket_name", Text)])


class EventRecord(EventRecordBase):
    def __new__(cls, **kargs):
        kargs['object_key'] = urllib.parse.unquote(kargs['object_key'])
        self = super(EventRecord, cls).__new__(cls, **kargs)
        return self
