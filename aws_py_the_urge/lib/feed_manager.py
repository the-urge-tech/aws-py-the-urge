import gzip
import logging

from aws_py_the_urge.lib.local_file_manager import LocalFileManager
from aws_py_the_urge.lib.s3_manager import S3Manager, S3Object
from aws_py_the_urge.settings import FILE_EXTENSION

LOG = logging.getLogger(__name__)


class FeedManager(S3Manager):
    def __init__(self, retailer_code, bucket_name,
                 aws_region='ap-southeast-2'):
        super(FeedManager, self).__init__(bucket_name, aws_region)
        self._retailer_code = retailer_code

    def find_last_feed(self):
        prefix = "format=original/retailer_code={}".format(self._retailer_code)
        newest_feed = self.find_last_obj(prefix, FILE_EXTENSION)
        return newest_feed

    def get_last_feed_content(self):
        newest_s3_object = S3Object(self.find_last_feed())
        if not newest_s3_object:
            return []
        local_feed_output_path = "/tmp/feedsldtos3/{}".format(
            newest_s3_object.path)
        local_feed_output_file = "{}/{}".format(local_feed_output_path,
                                                newest_s3_object.filename)
        LOG.info("Last feed comparing with is in: {}".format(
            local_feed_output_file))
        LOG.debug("Key={}".format(newest_s3_object.obj.key))
        self.download(newest_s3_object.obj.key, local_feed_output_path,
                      newest_s3_object.filename)
        return LocalFileManager(local_feed_output_file).get_feed_content()

    def put(self, path, body):
        self.put_into_s3_object(path, body)

    def is_equal_to_last(self, new_feed_gz):
        last_feed_content = self.get_last_feed_content()
        new_feed = gzip.decompress(new_feed_gz)
        return new_feed == last_feed_content
