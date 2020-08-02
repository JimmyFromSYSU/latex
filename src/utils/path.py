#!/usr/bin/python
# -*- coding: UTF-8 -*-
from typing import List, Optional
from os import listdir
from os.path import isfile, join


# TODO: also need to get all files


# TODO; return all folders/files in path
def _get_items(path: str) -> List[str]:
    # onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    return listdir(path)


# TODO: read from index file, clean all comments and empty line
def _get_index_list(path: str) -> Optional[List[str]]:
    return None


def get_sections(path: str) -> List[str]:
    index_list = _get_index_list(path)
    if index_list:
        return index_list
    else:
        return _get_items(path)


def read(file: str) -> str:
    print(file)
    result = ""
    with open(file, 'r') as input_file:
        result = input_file.read()
    return result


def write(file: str, content: str) -> str:
    with open(file, 'w') as output_file:
        result = output_file.write(content)
