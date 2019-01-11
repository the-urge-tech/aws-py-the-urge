import logging
from typing import Any, NamedTuple, Text

from aws_py_the_urge.lib.s3_parent import S3Parent
from aws_py_the_urge.util.path_manager import split_path
from aws_py_the_urge.util.date import get_newest_file

LOG = logging.getLogger(__name__)

S3Object = NamedTuple("S3Object", [("obj", Any), ("size", int), ("path", Text),
                                   ("filename", Text)])


class S3Manager(S3Parent):
    def __init__(self, bucket_name, aws_region='ap-southeast-2'):
        super(S3Manager, self).__init__(bucket_name, aws_region)

    def get_list_files_contain(self, prefix, name_file_expected: list):
        matching_paths = []
        list_path_files = self.get_list_all_files(prefix)
        for name_expected in name_file_expected:
            matching_paths += [
                file for file in list_path_files if name_expected in file
            ]
        return matching_paths

    def get_s3_object(self, prefix):
        s3_object_received = self._s3_resource.Object(self._bucket_name,
                                                      prefix)
        LOG.debug("obj:{}".format(s3_object_received))

        size = S3Manager.__get_size_s3_object(s3_object_received)
        newest_path, newest_filename = split_path(prefix)

        s3_object = S3Object(
            obj=s3_object_received,
            size=size,
            path=newest_path,
            filename=newest_filename)
        LOG.debug("S3Object: {}".format(s3_object))

        return s3_object

    def put_into_s3_object(self, path, body):
        LOG.debug("Put in {}/{}".format(self._bucket_name, path))
        self._s3_resource.Object(self._bucket_name, path).put(Body=body)

    def find_last_obj(self, prefix, file_extension):
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
        try:
            size = s3_object.content_lengt
            LOG.debug("s3_object size:{}".format(size))
            return size
        except Exception as e:
            LOG.exception(e)
            return 0
