#!/usr/bin/python
# -*- coding: UTF-8 -*-
LOGGER_FORMAT = '[%(asctime)s] %(message)s'


class BlockType():
    Text = "Text"
    Quote = "Quote"
    List = "List"
    NumberList = "NumberList"
    Math = "Math"
    Code = "Code"


class ListType():
    Normal = 0
    Number = 1
