import gzip
import json
import logging
import os
from pathlib import Path

from aws_py_the_urge.lib.s3_manager.file_manager import FileManager

LOG = logging.getLogger(__name__)


def write_gzip(items, key, local_prefix):
    return write_jl_gzip(items, key, local_prefix)


def write_jl_gzip(items, key, local_prefix, filter_keys=[]):
    local_output_path = os.path.dirname("{}{}".format(local_prefix, key))
    local_output = "{}{}".format(local_prefix, key)
    Path(local_output_path).mkdir(parents=True, exist_ok=True)
    with gzip.open(local_output, "wb") as f:
        for i in items:
            if len(filter_keys) > 0:
                i = {k: v for k, v in i.items() if k not in filter_keys}
            f.write((json.dumps(i) + "\n").encode("utf-8"))
    return local_output


def s3_upload(bucket_name, key, local_file, aws_region="us-east-1"):
    s3_file_manager = FileManager(bucket_name, aws_region)
    return s3_file_manager.upload(key, local_file)
