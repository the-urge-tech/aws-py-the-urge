import logging
import re
from datetime import date
from pathlib import Path
from typing import Any, NamedTuple, Text

import boto3

from aws_py_the_urge.util.date import path_date_extractor

LOG = logging.getLogger(__name__)

S3Object = NamedTuple("S3Object", [("obj", Any), ("path", Text),
                                   ("filename", Text)])


class S3Manager(object):
    def __init__(
            self,
            bucket_name,
            retailer_code,
    ):
        self._retailer_code = retailer_code
        self._s3 = boto3.resource('s3')
        self._bucket_name = bucket_name
        self._bucket = self._s3.Bucket(self._bucket_name)

    def find_newest_feed(self):
        newest_date = date(1, 1, 1)
        newest_obj = None
        newest_path = None
        newest_filename = None
        for obj in self._bucket.objects.filter(
                Prefix="format=original/retailer_code={}".format(
                    self._retailer_code)):
            LOG.debug(obj)
            current_date = path_date_extractor(obj.key)
            if current_date > newest_date:
                newest_date = current_date
                newest_obj = obj
                newest_matches = re.search(
                    '.*?\/(year=.*?\/month=.*?\/day=.*?)\/(.*)', obj.key)
                newest_path = newest_matches.group(1)
                newest_filename = newest_matches.group(2)
        return S3Object(
            obj=newest_obj, path=newest_path, filename=newest_filename)

    def download(self, key, local_output_path, local_output):
        if not Path(local_output).exists():
            Path(local_output_path).mkdir(parents=True, exist_ok=True)
            # TODO if does not exists
            LOG.debug("Downloading S3: {} to Local: {}".format(
                key, local_output))
            self._s3.Object(self._bucket_name, key).download_file(local_output)
