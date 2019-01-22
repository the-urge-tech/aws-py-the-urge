import logging
from pathlib import Path

from aws_py_the_urge.lib.s3_manager.s3_parent import S3Parent

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

    def get_list_all_files(self, prefix):
        """
        Get the list of all the files contained in prefix.
        :param prefix: s3 prefix.
        :return: list of files.
        """
        list_objects = self._s3_client.list_objects_v2(
            Bucket=self._bucket_name, Prefix=prefix)
        list_path_files = [
            file['Key'] for file in list_objects.get('Contents', [])
        ]
        return list_path_files

    def get_list_files_contain(self, prefix, name_file_expected: list):
        """
        Get the file list contained in prefix that contain name_file_expected in the name.
        :param prefix: s3 prefix.
        :param name_file_expected: string to use as fileter. 
        :return: list of files.
        """
        matching_paths = []
        list_path_files = self.get_list_all_files(prefix)
        for name_expected in name_file_expected:
            matching_paths += [
                file for file in list_path_files if name_expected in file
            ]
        return matching_paths

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
        object = self._s3_client.head_object(Bucket=self._bucket_name, Key=key)
        return object.get('Metadata', None)
