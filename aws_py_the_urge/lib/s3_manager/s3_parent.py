import logging
import boto3
from botocore.config import Config

LOG = logging.getLogger(__name__)

# cache it in the lambda global
cache_s3_client = {}
cache_s3_resource = {}


class S3Parent(object):
    def __init__(self, bucket_name, aws_region="us-east-1"):
        self._bucket_name = bucket_name
        if not cache_s3_client.get(aws_region, False):
            cache_s3_client[aws_region] = boto3.client(
                "s3", aws_region, config=Config(s3={"addressing_style": "path"})
            )
        if not cache_s3_resource.get(aws_region, False):
            cache_s3_resource[aws_region] = boto3.resource(
                "s3", aws_region, config=Config(s3={"addressing_style": "path"})
            )

        self._s3_client = cache_s3_client[aws_region]
        self._s3_resource = cache_s3_resource[aws_region]
        self._bucket = self._s3_resource.Bucket(self._bucket_name)
