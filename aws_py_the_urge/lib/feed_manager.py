import gzip
import logging
from zipfile import ZipFile

from aws_py_the_urge.lib.local_file_manager import LocalFileManager
from aws_py_the_urge.lib.s3_manager.object_manager import ObjectManager, S3Object

LOG = logging.getLogger(__name__)


class FeedManager(ObjectManager):
    def __init__(self, retailer_code, bucket_name,
                 aws_region='ap-southeast-2'):
        super(FeedManager, self).__init__(bucket_name, aws_region)
        self._retailer_code = retailer_code

    def find_last_feed(self, file_extension):
        prefix = "format=original/retailer_code={}".format(self._retailer_code)
        newest_feed = self.find_last_obj(prefix, file_extension)
        return newest_feed

    def get_last_feed_content(self, file_extension,
                              last_feed: S3Object = None):
        if not last_feed:
            last_feed = S3Object(self.find_last_feed(file_extension))
        if not last_feed:
            return []
        local_feed_output_path = "/tmp/feedsldtos3/{}".format(last_feed.path)
        local_feed_output_file = "{}/{}".format(local_feed_output_path,
                                                last_feed.filename)
        LOG.debug(
            "Last feed is downloading in: {}".format(local_feed_output_file))
        LOG.debug("Key={}".format(last_feed.obj.key))
        self.download(last_feed.obj.key, local_feed_output_path,
                      last_feed.filename)
        return LocalFileManager(local_feed_output_file).get_feed_content()

    def put(self, path, body):
        self.put_into_s3_object(path, body)

    def is_equal_to_last(self, new_feed, file_extension):
        last_feed_content = self.get_last_feed_content(file_extension)
        if file_extension == '.gz':
            new_feed_decompress = gzip.decompress(new_feed)
            return new_feed_decompress == last_feed_content
        elif file_extension == ".zip":
            z = ZipFile(new_feed)
            zfile = z.namelist()[0]
            new_feed_decompress = zfile.read(zfile)
            return new_feed == new_feed_decompress
        return new_feed == last_feed_content
