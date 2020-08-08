#!/usr/bin/python
# -*- coding: UTF-8 -*-
from typing import List, Optional
from os import listdir
from os.path import isfile, join

def read(file: str) -> str:
    result = ""
    with open(file, 'r') as input_file:
        result = input_file.read()
    return result


def write(file: str, content: str) -> str:
    with open(file, 'w') as output_file:
        result = output_file.write(content)


def trim_ext(file: str) -> str:
    return os.path.splitext(file)[0]
