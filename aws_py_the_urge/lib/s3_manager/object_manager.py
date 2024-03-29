import logging
from datetime import date
from collections import namedtuple

from aws_py_the_urge.lib.s3_manager.file_manager import FileManager
from aws_py_the_urge.util.date import get_newest_file, path_date_extractor
from aws_py_the_urge.util.path_manager import split_path

LOG = logging.getLogger(__name__)

S3Object = namedtuple("S3Object", ["obj", "size", "date", "path", "filename"])


class ObjectManager(FileManager):
    def __init__(self, bucket_name, aws_region="us-east-1"):
        super(ObjectManager, self).__init__(bucket_name, aws_region)

    def download_body(self, prefix):
        """
        Download the body of an object in s3
        :param prefix: file prefix in s3.
        :return: bytes
        """
        waiter = self._s3_client.get_waiter("object_exists")
        waiter_config = {"Delay": 1, "MaxAttempts": 10}
        waiter.wait(Bucket=self._bucket_name, Key=prefix, WaiterConfig=waiter_config)
        s3_object_received = self._s3_resource.Object(self._bucket_name, prefix)
        body = s3_object_received.get().get("Body", None)
        if body:
            return body.read()
        else:
            LOG.error(
                "Could not read the streaming_body of {}{} body is: {} even though we waited with config {} ".format(
                    self._bucket_name, prefix, body, waiter_config
                )
            )
        return body

    def get_s3_object(self, prefix):
        """
        Get the S3Object from s3. ATTENTION: method useful only if prefix is like ../year=2019/month=4/day=23/...
        :param prefix: file prefix in s3.
        :return: S3Object.
        """
        s3_object_received = self._s3_resource.Object(self._bucket_name, prefix)
        LOG.debug("obj:{}".format(s3_object_received))

        size = ObjectManager.__get_size_s3_object(s3_object_received)
        newest_path, newest_filename = split_path(prefix)
        date_file = path_date_extractor(prefix)

        s3_object = S3Object(
            obj=s3_object_received,
            size=size,
            date=date_file,
            path=newest_path,
            filename=newest_filename,
        )
        LOG.debug("S3Object: {}".format(s3_object))

        return s3_object

    def put_into_s3_object(
        self,
        path: str,
        body,
        metadata: dict = None,
        content_type: str = None,
        cache_control: str = None,
    ):
        """
        Upload the body into the s3 file.
        :param path: file path in s3.
        :param body: body file.
        :param metadata: metadata of of the object
        :param content_type: content type of the object
        """
        LOG.debug("Put in {}/{}".format(self._bucket_name, path))
        if content_type and metadata:
            self._s3_resource.Object(self._bucket_name, path).put(
                Body=body,
                Metadata={k: str(v) for k, v in metadata.items()},
                ContentType=content_type,
                CacheControl=cache_control,
            )
        else:
            self._s3_resource.Object(self._bucket_name, path).put(Body=body)

        waiter = self._s3_client.get_waiter("object_exists")
        waiter_config = {"Delay": 1, "MaxAttempts": 10}
        waiter.wait(Bucket=self._bucket_name, Key=path, WaiterConfig=waiter_config)

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
                "The s3 path list does not contain any file with extension {}. List: {}".format(
                    file_extension, list_objects
                )
            )
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
