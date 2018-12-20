import glob
import gzip
import json
import logging
import os
import random
from zipfile import ZipFile

from aws_py_the_urge.lib.s3_manager import S3Manager

LOG = logging.getLogger(__name__)


def s3_download(bucket_name, key, local_path, aws_region='ap-southeast-2'):
    s3_manager = S3Manager(bucket_name, aws_region)
    return s3_manager.download(key, local_path, key)


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
    jls = []
    for f in glob.glob("{}/*.jl.gz".format(folder_path)):
        gz_path = os.path.join(root_test, '../', folder_path, f)
        print('gz_path')
        print(gz_path)
        jls = jls + read_jl_zip(gz_path, '')
    return jls
