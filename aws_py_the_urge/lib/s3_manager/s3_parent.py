import logging
import pathlib
import boto3

from aws_xray_sdk.core import xray_recorder  # invoked automagically for lambda https://docs.aws.amazon.com/xray-sdk-for-python/latest/reference/basic.html#aws-lambda-integration
from aws_xray_sdk.core import patch_all
from botocore.config import Config

LOG = logging.getLogger(__name__)

if "parsers/" in pathlib.Path(__file__).parent.resolve():
    patch_all()

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
