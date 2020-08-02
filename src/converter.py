#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .md_tree import MDDocument
from .render.md_tex_render import MDTexRender


def md2tex(input: str, level: int) -> str:
    doc = MDDocument(input)
    doc.parse()
    tex_render = MDTexRender(level)
    return doc.render_with(tex_render)


def md2html(input: str, level: int) -> str:
    # TODO:
    return ""


def md2word(input: str, level: int) -> str:
    # TODO:
    return ""
