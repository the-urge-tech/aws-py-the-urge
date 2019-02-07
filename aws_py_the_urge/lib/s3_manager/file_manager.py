import logging
from pathlib import Path
from typing import NamedTuple, Text
from datetime import datetime

from aws_py_the_urge.lib.s3_manager.s3_parent import S3Parent

FileS3 = NamedTuple("FileS3", [("key", Text), ("last_modify", datetime),
                               ("meta", dict)])

LOG = logging.getLogger(__name__)


class FileManager(S3Parent):
    def __init__(self, bucket_name, aws_region='ap-southeast-2'):
        super(FileManager, self).__init__(bucket_name, aws_region)

    def download(self, key, local_path, file_name):
        """
        Download file from s3 bucket.
        :param key: s3 key.
        :param local_path: folder where the file will download in.
        :param file_name: file name with extestion.
        :return: file path where the file is saved.
        """
        if not Path(local_path).exists():
            Path(local_path).mkdir(parents=True, exist_ok=True)
        local_file_output = '{}/{}'.format(local_path, file_name)
        LOG.debug("Downloading S3: {}/{} to Local: {}".format(
            self._bucket_name, key, local_file_output))
        self._s3_client.download_file(self._bucket_name, key,
                                      local_file_output)
        LOG.debug("Downloaded in: {}".format(local_file_output))
        return local_file_output

    def upload(self, key, local_file):
        """
        Upload file into s3.
        :param key: s3 key.
        :param local_file: path of the local file.
        :return: local_file .
        """
        LOG.debug("Uploading Local: {} to S3: {}/{}".format(
            local_file, self._bucket_name, key))
        self._s3_client.upload_file(local_file, self._bucket_name, key)
        return local_file

    def get_list_all_files(self, prefix, with_meta=False):
        """
        Get the list of all the files contained in prefix.
        :param prefix: s3 prefix.
        :param with_meta if true the matadata is included within the result.
        :return: list of files.
        """
        list_objects = self._s3_client.list_objects_v2(
            Bucket=self._bucket_name, Prefix=prefix)
        if with_meta:
            list_path_all_files = [
                FileS3(
                    key=file['Key'],
                    last_modify=file['LastModified'],
                    meta=self.get_metadata(file['Key']))
                for file in list_objects.get('Contents', [])
            ]
        else:
            list_path_all_files = [
                FileS3(
                    key=file['Key'], last_modify=file['LastModified'], meta={})
                for file in list_objects.get('Contents', [])
            ]
        LOG.debug("list_path_all_files: {}".format(list_path_all_files))
        return list_path_all_files

    def get_list_files_contain(self,
                               prefix,
                               name_file_expected: list,
                               with_meta=False):
        """
        Get the file list contained in prefix that contain name_file_expected in the name.
        :param prefix: s3 prefix.
        :param name_file_expected: string to use as fileter.
        :param with_meta if true the matadata is included within the result.
        :return: list of files.
        """
        matching_files = []
        list_path_files = self.get_list_all_files(prefix)
        for name_expected in name_file_expected:
            matching_files += [
                file for file in list_path_files if name_expected in file.key
            ]
        if with_meta:
            for file in matching_files:
                file.meta = self.get_metadata(file.key)
        LOG.debug("list_path_files: {}".format(list_path_files))
        return matching_files

    def exists(self, prefix):
        """
        Check if the prefix exists. A prefix exists iff it contains at list one file.
        :param prefix: s3 prefix.
        :return: boolean
        """
        return len(self.get_list_all_files(prefix)) > 0

    def get_metadata(self, key):
        """
        Get the metadata of a file in s3 given the key.
        :param key: s3 key.
        :return: dict of the metadata.
        """
        try:
            obj = self._s3_client.head_object(
                Bucket=self._bucket_name, Key=key)
            return obj.get('Metadata', None)
        except Exception as e:
            LOG.warning(
                "File not found or connection error. Key:{} Error:{}".format(
                    key, e))
            return None

    def copy(self, origin_key, destination_key):
        """
        Copy the object in the new folder.
        :param origin_key: key of the copy source
        :param destination_key: key of the destination source
        :return:
        """
        copy_source = {'Bucket': self._bucket_name, 'Key': origin_key}
        response = self._s3_client.copy_object(
            Bucket=self._bucket_name,
            CopySource=copy_source,
            Key=destination_key)
        return response['CopyObjectResult']

    def move(self, origin_key, destination_key):
        """
        Copy the object in the new folder and delete the old one.
        :param origin_key: key of the copy source
        :param destination_key: key of the destination source
        :return:
        """
        response_copy = self.copy(origin_key, destination_key)
        LOG.debug("response_copy: {}".format(response_copy))
        return self.delete([origin_key])

    def delete(self, list_keys: list):
        """
        Delete up to 1000 object from s3.
        :param list_keys: list of the keys object to delete
        :return:
        """
        LOG.warning("You are deleting: {}".format(list_keys))
        keys = {'Objects': [{'Key': k} for k in list_keys]}
        response = self._s3_client.delete_objects(
            Bucket=self._bucket_name, Delete=keys)
        if 'Deleted' in response:
            LOG.warning("Files deleted: {}".format(response['Deleted']))
        if 'Errors' in response:
            LOG.warning("Errors deleted files: {}".format(response['Errors']))
        return response
