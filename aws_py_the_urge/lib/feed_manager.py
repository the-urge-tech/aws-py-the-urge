import gzip
import logging
from typing import Any, NamedTuple, Text

from aws_py_the_urge.lib.local_file_manager import LocalFileManager
from aws_py_the_urge.lib.s3_manager import S3Manager
from aws_py_the_urge.util.date import get_newest_file
from aws_py_the_urge.util.path_manager import split_path
from aws_py_the_urge.settings import FILE_EXTENSION

LOG = logging.getLogger(__name__)

S3Object = NamedTuple("S3Object", [("obj", Any), ("path", Text),
                                   ("filename", Text)])


class FeedManager(S3Manager):
    def __init__(self, retailer_code, bucket_name,
                 aws_region='ap-southeast-2'):
        super(FeedManager, self).__init__(bucket_name, aws_region)
        self._retailer_code = retailer_code

    def find_newest_feed(self):
        prefix = "format=original/retailer_code={}".format(self._retailer_code)
        list_objects = self.get_list_all_files(prefix=prefix)
        LOG.debug("list_objects:{}".format(list_objects))
        if not list_objects:
            LOG.warning("No files found in {}".format(prefix))
            return []

        prefix_newest_obj = get_newest_file(list_objects, FILE_EXTENSION)
        LOG.debug("prefix_newest_obj:{}".format(prefix_newest_obj))
        if not prefix_newest_obj:
            LOG.error(
                "The s3 path list does not contain any file with extension {}. List: {}"
                .format(FILE_EXTENSION, list_objects))
            return []

        newest_obj = self._s3_resource.Object(self._bucket_name,
                                              prefix_newest_obj)
        LOG.debug("newest_obj:{}".format(newest_obj))

        newest_path, newest_filename = split_path(prefix_newest_obj)
        s3_object = S3Object(
            obj=newest_obj, path=newest_path, filename=newest_filename)
        LOG.debug("S3Object: {}".format(s3_object))

        return s3_object

    def put(self, output, body):
        LOG.debug("Put in {}/{}".format(self._bucket_name, output))
        self._s3_resource.Object(self._bucket_name, output).put(Body=body)

    def is_equal_to_last(self, new_feed_gz):
        last_feed_content = self.get_last_feed_content()
        new_feed = gzip.decompress(new_feed_gz)
        return new_feed == last_feed_content

    def get_last_feed_content(self):
        newest_s3_object = self.find_newest_feed()
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
