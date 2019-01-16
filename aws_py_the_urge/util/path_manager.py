import os
import logging

LOG = logging.getLogger(__name__)


def split_path(path: str):
    directory, file_name = os.path.split(path)
    LOG.debug("directory:{}".format(directory))
    LOG.debug("newest_filename:{}".format(file_name))
    return directory, file_name


def get_exension(file_name: str):
    _, file_extension = os.path.splitext(file_name)
    return file_extension
