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

    def find_last_feed(self, file_extension=""):
        prefix = "format=original/retailer_code={}".format(self._retailer_code)
        newest_feed = self.find_last_obj(prefix, file_extension)
        return newest_feed

    def get_last_feed_content(self,
                              file_extension="",
                              last_feed: S3Object = None,
                              binary=False):
        """
        Get the up to date new_feed on s3
        :param file_extension: it is possible to define the extension to filter the search
        :param last_feed: you can give S3Object where extract the content from 
        :param binary: if True the return data is given without decompression
        :return: 
        """
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
        if binary:
            LocalFileManager(local_feed_output_file).get_feed_content_binary()

        return LocalFileManager(local_feed_output_file).get_feed_content()

    def put(self, path, body):
        self.put_into_s3_object(path, body)

    def is_equal_to_last(self, new_feed, file_extension="", binary=True):
        """
        Compare new_feed with the up to date fide on s3
        :param new_feed: feed content just downloaded 
        :param file_extension: it is possible to define the extension to filter the search
        :param binary: if True the comparision is going to be done without decompression
        :return: 
        """
        last_feed_content = self.get_last_feed_content(
            file_extension, binary=binary)
        if binary:
            return new_feed == last_feed_content

        if file_extension == '.gz':
            new_feed_decompress = gzip.decompress(new_feed)
            return new_feed_decompress == last_feed_content
        elif file_extension == ".zip":
            z = ZipFile(new_feed)
            zfile = z.namelist()[0]
            new_feed_decompress = zfile.read(zfile)
            return new_feed == new_feed_decompress
        else:
            LOG.warning(
                "File extension {} is not neither gz or zip. The file could not be decompressed."
            )
            return new_feed == last_feed_content
