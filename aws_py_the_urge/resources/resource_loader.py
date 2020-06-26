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
        return None
    LOG.debug("Loading file: %s", file_path)
    return open(file_path).read()


def load_json_input(folder, filename) -> Any:
    """
    Load a file relative to the resources folder
    :return: a NamedTuple input_data of type Input
    """
    content = load_input(folder, filename)
    if content is None:
        return None
    return json.loads(content)


def load(folder=None, input_filename=None):
    return load_json_input(folder, input_filename)


def load_slug_rule(language):
    lang_dict = {
        "arabic.json": ["ar"],
        "armenian.json": ["hy"],
        "austrian.json": [],
        "azerbaijani.json": ["az"],
        "bulgarian.json": ["bg"],
        "burmese.json": ["my"],
        "chinese.json": ["zh"],
        "croatian.json": ["hr"],
        "czech.json": ["cs"],
        "danish.json": ["da"],
        "default.json": ["zz"],
        "esperanto.json": ["eo"],
        "estonian.json": ["et"],
        "finnish.json": ["fi"],
        "french.json": ["fr"],
        "georgian.json": ["ka"],
        "german.json": ["de"],
        "greek.json": ["el"],
        "hindi.json": ["hi"],
        "hungarian.json": ["hu"],
        "italian.json": ["it"],
        "latvian.json": ["lv"],
        "lithuanian.json": ["lt"],
        "macedonian.json": ["mk"],
        "norwegian.json": ["no"],
        "persian.json": ["fa"],
        "polish.json": ["pl"],
        "portuguese-brazil.json": ["pt"],
        "romanian.json": ["ro"],
        "russian.json": ["ru"],
        "serbian.json": ["sr"],
        "slovak.json": ["sk"],
        "swedish.json": ["sv"],
        "turkish.json": ["tr"],
        "turkmen.json": ["tk"],
        "ukrainian.json": ["uk"],
        "vietnamese.json": ["vi"],
    }
    for k, v in lang_dict.items():
        if language in v:
            return load_json_input("slug_rules", k)
    return None
