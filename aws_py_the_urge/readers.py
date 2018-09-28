import gzip
import json
import logging
import os
import random
from pathlib import Path
from zipfile import ZipFile

import boto3

LOG = logging.getLogger(__name__)


def s3_download(bucket_name, key):
    local_output_path = os.path.dirname("/tmp/parsers/fetched/{}".format(key))
    local_output = "/tmp/parsers/fetched/{}".format(key)
    Path(local_output_path).mkdir(parents=True, exist_ok=True)
    LOG.info("Downloading S3: {}/{} to Local: {}".format(
        bucket_name, key, local_output))
    print('downloading test print')
    s3 = boto3.resource('s3')
    s3.Object(bucket_name, key).download_file(local_output)
    return local_output


def read_jl_zip(zipfile, jlfile, sample=0):
    if zipfile.endswith('.gz'):
        # GZIP DOES NOT NEED THE FILENAME INSIDE THE ARCHIVE. GOOD
        with gzip.open(zipfile, 'rb') as data_file:
            return _read_lines(data_file, sample)
    else:
        with ZipFile(zipfile) as myzip:
            with myzip.open(jlfile, 'r') as data_file:
                return _read_lines(data_file, sample)


def read_jl(jlfile, sample=0):
    jl = []
    with open(jlfile, 'r') as data_file:
        jl = _read_lines(data_file, sample)
    return jl


def _read_lines(data_file, sample):
    jl = []
    if sample == 0:
        lines = data_file.readlines()
    else:
        try:
            lines = random.sample(data_file.readlines(), sample)
        except:
            lines = data_file.readlines()
    for line in lines:
        jl.append(json.loads(line))
    return jl
