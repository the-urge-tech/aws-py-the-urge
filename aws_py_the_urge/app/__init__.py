"""aws_py_the_urge - An opinionated, minimal cookiecutter template for Python packages"""

__version__ = '0.1.0'
__author__ = 'the urge <pierre.caserta@gmail.com>'
__all__ = []

import re
import urllib.parse
from typing import NamedTuple, Text

EventRecordBase = NamedTuple(
    "EventRecordBase", [("object_key", Text), ("event_name", Text),
                        ("bucket_name", Text), ("named_tmp_file_id", Text),
                        ("retailer_code", Text)])


# TODO not a good usage of namedtuple
# this should be a normal class
class EventRecord(EventRecordBase):
    def __new__(cls, **kargs):
        object_key = urllib.parse.unquote(kargs['object_key'])
        kargs['object_key'] = object_key
        matches = re.search('.*?\/retailer_code=(.*?)\/.*', object_key)
        kargs['retailer_code'] = matches.group(1)
        matches = re.search('.*?--fetched--(.*?)\..*', object_key)
        if matches:
            kargs['named_tmp_file_id'] = matches.group(1)
        matches = re.search('.*?--parsed--(.*?)\..*', object_key)
        if matches:
            kargs['named_tmp_file_id'] = matches.group(1)
        matches = re.search('.*?--enriched--(.*?)\..*', object_key)
        if matches:
            kargs['named_tmp_file_id'] = matches.group(1)
        self = super(EventRecord, cls).__new__(cls, **kargs)
        return self
