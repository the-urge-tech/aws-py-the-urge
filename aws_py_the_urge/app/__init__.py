"""aws_py_the_urge - An opinionated, minimal cookiecutter template for Python packages"""

__version__ = "0.1.0"
__author__ = "the urge <pierre.caserta@gmail.com>"
__all__ = []

import logging
import re
import urllib.parse
from collections import namedtuple

LOG = logging.getLogger(__name__)
EventRecordBase = namedtuple(
    "EventRecordBase",
    [
        "object_key",
        "event_name",
        "bucket_name",
        "named_tmp_file_id",
        "type",
    ],
)


# TODO not a good usage of namedtuple
# this should be a normal class
class EventRecord(EventRecordBase):
    def __new__(cls, **kargs):
        try:
            object_key = urllib.parse.unquote(kargs["object_key"])
            kargs["object_key"] = object_key
            matches = re.search(
                r"type=(.*?)/.*/.*__.*--.*--(.*?)\..*?",
                object_key,
            )
            kargs["type"] = matches.group(1)
            kargs["named_tmp_file_id"] = matches.group(2)
            self = super(EventRecord, cls).__new__(cls, **kargs)
            return self
        except Exception as e:
            LOG.error(
                "Error while creating EventRecord in aws-py-the-urge: {}\nkargs: {}".format(
                    e, kargs
                ),
                exc_info=True,
            )
