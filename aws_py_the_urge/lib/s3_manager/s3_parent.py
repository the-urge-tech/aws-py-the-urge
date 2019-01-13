import logging
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
