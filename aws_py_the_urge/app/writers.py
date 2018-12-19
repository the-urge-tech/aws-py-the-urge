import gzip
import json
import logging
import os
from pathlib import Path

import boto3
from botocore.config import Config

LOG = logging.getLogger(__name__)


def write_gzip(items, key, local_prefix):
    return write_jl_gzip(items, key, local_prefix)


def write_jl_gzip(items, key, local_prefix):
    local_output_path = os.path.dirname("{}{}".format(local_prefix, key))
    local_output = "{}{}".format(local_prefix, key)
    Path(local_output_path).mkdir(parents=True, exist_ok=True)
    with gzip.open(local_output, 'wb') as f:
        for i in items:
            f.write((json.dumps(i) + '\n').encode('utf-8'))
    return local_output


def s3_upload(bucket_name, key, local_file, aws_region='ap-southeast-2'):
    LOG.info("Uploading Local: {} to S3: {}/{}".format(local_file, bucket_name,
                                                       key))
    s3 = boto3.client(
        's3', aws_region, config=Config(s3={'addressing_style': 'path'}))
    s3.upload_file(local_file, bucket_name, key)
    return local_file
