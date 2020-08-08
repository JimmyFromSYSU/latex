#!/usr/bin/python
# -*- coding: UTF-8 -*-


class ListType():
    Normal = 0
    Number = 1


class InLineType():
    Normal = 0
    Link = 1
    Bold = 2
    Include = 3
    Image = 4  # real image such as jpg, png


class IncludeType():
    Text = "text"
    Image = "image"  # tex file image
    Code = "code"
    Dot = "dot" # https://graphviz.org/doc/info/lang.html


DOT_IMAGE_TYPE = "eps" # png/pdf/jpg won't create bounding box
