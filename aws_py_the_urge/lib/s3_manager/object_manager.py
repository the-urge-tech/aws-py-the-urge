import logging
from datetime import date
from typing import Any, NamedTuple, Text

from aws_py_the_urge.util.path_manager import split_path
from aws_py_the_urge.util.date import get_newest_file, path_date_extractor
from aws_py_the_urge.lib.s3_manager.file_manager import FileManager

LOG = logging.getLogger(__name__)

S3Object = NamedTuple("S3Object", [("obj", Any), ("size", int), ("date", date),
                                   ("path", Text), ("filename", Text)])


class ObjectManager(FileManager):
    def __init__(self, bucket_name, aws_region='ap-southeast-2'):
        super(ObjectManager, self).__init__(bucket_name, aws_region)

    def get_s3_object(self, prefix):
        """
        Get the S3Object from s3.
        :param prefix: file prefix in s3.
        :return: S3Object.
        """
        s3_object_received = self._s3_resource.Object(self._bucket_name,
                                                      prefix)
        LOG.debug("obj:{}".format(s3_object_received))

        size = ObjectManager.__get_size_s3_object(s3_object_received)
        newest_path, newest_filename = split_path(prefix)
        date_file = path_date_extractor(prefix)

        s3_object = S3Object(
            obj=s3_object_received,
            size=size,
            date=date_file,
            path=newest_path,
            filename=newest_filename)
        LOG.debug("S3Object: {}".format(s3_object))

        return s3_object

    def put_into_s3_object(self, path, body):
        """
        Upload the body into the s3 file.
        :param path: file path in s3.
        :param body: body file.
        """
        LOG.debug("Put in {}/{}".format(self._bucket_name, path))
        self._s3_resource.Object(self._bucket_name, path).put(Body=body)

    def find_last_obj(self, prefix, file_extension):
        """
        Get the last S3Object from s3 ordered by date.
        :param prefix: path contains the files.
        :param file_extension: file extension for filtering.
        :return: last S3Object up to date.
        """
        list_objects = self.get_list_all_files(prefix=prefix)
        LOG.debug("list_objects:{}".format(list_objects))
        if not list_objects:
            LOG.warning("No files found in {}".format(prefix))
            return []

        prefix_newest_obj = get_newest_file(list_objects, file_extension)
        LOG.debug("prefix_newest_obj:{}".format(prefix_newest_obj))
        if not prefix_newest_obj:
            LOG.error(
                "The s3 path list does not contain any file with extension {}. List: {}"
                .format(file_extension, list_objects))
            return []
        return self.get_s3_object(prefix_newest_obj)

    @staticmethod
    def __get_size_s3_object(s3_object):
        """
        Private method to get the S3Object size.
        :param s3_object: S3Object.
        :return: S3Object size.
        """
        try:
            size = s3_object.content_length
            LOG.debug("s3_object size:{}".format(size))
            return size
        except Exception as e:
            LOG.exception(e)
            return 0
