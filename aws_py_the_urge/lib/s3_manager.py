import logging
import os
from pathlib import Path
from typing import Any, NamedTuple, Text

import boto3
from botocore.config import Config

LOG = logging.getLogger(__name__)

S3Object = NamedTuple("S3Object", [("obj", Any), ("path", Text),
                                   ("filename", Text)])


class S3Manager(object):
    def __init__(self, bucket_name, aws_region='ap-southeast-2'):
        self._bucket_name = bucket_name
        self._s3_client = boto3.client(
            's3', aws_region, config=Config(s3={'addressing_style': 'path'}))
        self._s3_resource = boto3.resource(
            's3', aws_region, config=Config(s3={'addressing_style': 'path'}))
        self._bucket = self._s3_resource.Bucket(self._bucket_name)

    def download(self, key, local_path, file_name):
        # if not Path(local_output).exists():
        Path(local_path).mkdir(parents=True, exist_ok=True)
        # self._s3.Object(self._bucket_name,
        #                          key).download_file(local_output)
        local_file_output = '{}/{}'.format(local_path, file_name)
        LOG.info("Downloading S3: {}/{} to Local: {}".format(
            self._bucket_name, key, local_file_output))
        self._s3_client.download_file(self._bucket_name, key,
                                      local_file_output)
        LOG.info("Download: {}".format(local_file_output))
        return local_file_output

    def upload(self, key, local_file):
        LOG.info("Uploading Local: {} to S3: {}/{}".format(
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

    def get_list_files_contain(self, prefix, name_file_expected):
        assert type(name_file_expected) is list
        matching_paths = []
        list_path_files = self.get_list_all_files(prefix)
        for name_expected in name_file_expected:
            matching_paths += [
                file for file in list_path_files if name_expected in file
            ]
        return matching_paths

    def exists(self, prefix):
        return len(self.get_list_all_files(prefix)) > 0
