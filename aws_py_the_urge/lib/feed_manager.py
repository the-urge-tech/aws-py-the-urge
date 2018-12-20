import logging
from typing import Any, NamedTuple, Text
from datetime import date
import re
import gzip

from aws_py_the_urge.lib.s3_manager import S3Manager
from aws_py_the_urge.util.date import path_date_extractor
from aws_py_the_urge.lib.local_file_manager import LocalFileManager

LOG = logging.getLogger(__name__)

S3Object = NamedTuple("S3Object", [("obj", Any), ("path", Text),
                                   ("filename", Text)])


class FeedManager(S3Manager):
    def __init__(self, retailer_code, bucket_name,
                 aws_region='ap-southeast-2'):
        super(FeedManager, self).__init__(bucket_name, aws_region)
        self._retailer_code = retailer_code

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
        LOG.info("S3Object: {}, {}".format(newest_path, newest_filename))
        return S3Object(
            obj=newest_obj, path=newest_path, filename=newest_filename)

    def put(self, output, body):
        LOG.info("Put in {}/{}".format(self._bucket_name, output))
        self._s3_resource.Object(self._bucket_name, output).put(Body=body)

    def is_equal_to_last(self, new_feed_gz):
        last_feed_content = self.get_last_feed_content()
        new_feed = gzip.decompress(new_feed_gz)
        return new_feed == last_feed_content

    def get_last_feed_content(self):
        newest_s3_object = self.find_newest_feed()
        local_feed_output_path = "/tmp/feedsldtos3/{}".format(
            newest_s3_object.path)
        local_feed_output_file = "{}/{}".format(local_feed_output_path,
                                                newest_s3_object.filename)
        LOG.info("Last feed comparing with is in: {}".format(
            local_feed_output_file))
        LOG.info("Key={}".format(newest_s3_object.obj.key))
        self.download(newest_s3_object.obj.key, local_feed_output_path,
                      newest_s3_object.filename)
        return LocalFileManager(local_feed_output_file).get_feed_content()
