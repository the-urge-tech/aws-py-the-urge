import glob
import gzip
import json
import logging
import os
import random
from pathlib import Path
from zipfile import ZipFile

import boto3

LOG = logging.getLogger(__name__)


def s3_download(bucket_name, key, local_prefix):
    local_output_path = os.path.dirname("{}{}".format(local_prefix, key))
    local_output = "{}{}".format(local_prefix, key)
    Path(local_output_path).mkdir(parents=True, exist_ok=True)
    LOG.info("Downloading S3: {}/{} to Local: {}".format(
        bucket_name, key, local_output))
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


def load_gz(test_file_path, root_test, folder_name):
    yaml_name = os.path.basename(test_file_path).replace('_test.py',
                                                         '').replace('_', '-')
    folder_path = os.path.join(root_test, '../', "{}/{}".format(
        folder_name, yaml_name))
    os.chdir(folder_path)
    jls = []
    for f in glob.glob("*.jl.gz"):
        gz_path = os.path.join(root_test, '../', folder_path, f)
        print('gz_path')
        print(gz_path)
        jls = jls + read_jl_zip(gz_path, '')
    return jls
