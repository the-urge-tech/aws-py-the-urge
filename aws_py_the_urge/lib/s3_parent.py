import logging
from pathlib import Path
import boto3
from botocore.config import Config

LOG = logging.getLogger(__name__)


class S3Parent(object):
    def __init__(self, bucket_name, aws_region='ap-southeast-2'):
        self._bucket_name = bucket_name
        self._s3_client = boto3.client(
            's3', aws_region, config=Config(s3={'addressing_style': 'path'}))
        self._s3_resource = boto3.resource(
            's3', aws_region, config=Config(s3={'addressing_style': 'path'}))
        self._bucket = self._s3_resource.Bucket(self._bucket_name)

    def download(self, key, local_path, file_name):
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
        LOG.debug("Uploading Local: {} to S3: {}/{}".format(
            local_file, self._bucket_name, key))
        self._s3_client.upload_file(local_file, self._bucket_name, key)
        return local_file

    def get_list_all_files(self, prefix):
        list_objects = self._s3_client.list_objects_v2(
            Bucket=self._bucket_name, Prefix=prefix)
        list_path_files = [
            file['Key'] for file in list_objects.get('Contents', [])
        ]
        return list_path_files

    def exists(self, prefix):
        return len(self.get_list_all_files(prefix)) > 0
