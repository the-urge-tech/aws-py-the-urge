"""
This functions will load the input resources.
Loading resources can be source of errors so we use typing and NamedTuple to facilitate the development and testing.
"""
import collections
import json
import logging
import os
from os import listdir
from os.path import isfile, join
from typing import Any, NamedTuple

LOG = logging.getLogger(__name__)

Resource = collections.namedtuple("Resource", "path content")


def find_file_path(folder, filename):
    folder_path = os.path.join(os.path.dirname(__file__), folder)
    if not filename:
        files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
        filename = sorted(files)[-1]
    file_path = join(folder_path, filename)
    return file_path


def load_input(folder, filename) -> Any:
    """
    Load a file relative to the resources folder
    :return: a NamedTuple input_data of type Input
    """
    file_path = find_file_path(folder, filename)
    if not isfile(file_path):
        LOG.error("Not a file: %s", file_path)
        return Resource(path=None, content=None)
    LOG.debug("Loading file: %s", file_path)
    return Resource(path=file_path, content=open(file_path).read())


def load_json_input(folder, filename) -> Any:
    """
    Load a file relative to the resources folder
    :return: a NamedTuple input_data of type Input
    """
    resource = load_input(folder, filename)
    if resource.content is None:
        return resource
    return Resource(path=resource.path, content=json.loads(resource.content))


def load(folder=None, input_filename=None):
    return Resources(mapping=load_json_input(folder, input_filename))
