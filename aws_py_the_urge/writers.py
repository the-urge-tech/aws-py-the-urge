import gzip
import json
import logging
import os
from pathlib import Path

import boto3

LOG = logging.getLogger(__name__)


def write_gzip(items, key):
    local_output_path = os.path.dirname("/tmp/parsers/parsed/{}".format(key))
    local_output = "/tmp/parsers/parsed/{}".format(key)
    Path(local_output_path).mkdir(parents=True, exist_ok=True)
    with gzip.open(local_output, 'wb') as f:
        f.write(json.dumps(items).encode('utf-8'))
    return local_output


def s3_upload(bucket_name, key, local_file):
    LOG.info("Uploading Local: {} to S3: {}/{}".format(local_file, bucket_name,
                                                       key))
    s3 = boto3.client('s3')
    s3.upload_file(local_file, bucket_name, key)
    return local_file
