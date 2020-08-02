#!/usr/bin/python
# -*- coding: UTF-8 -*-
from src.utils.path import read
from src.render.latex import DOCUMENT
from src.md_tree import MDDocument
from src.render.md_tex_render import MDTexRender
import argparse
import logging
from src.constants import LOGGER_FORMAT
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format=LOGGER_FORMAT)


def test_single_tex_file(path, print_result: bool = False):
    article = read(path)
    doc = MDDocument(article)
    doc.parse()
    doc.print()
    tex_render = MDTexRender()
    if print_result:
        print("----------------------------------- render result:")
        print(doc.render_with(tex_render))


def get_args() -> argparse.Namespace:
    logger.info("Parse arguments.")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path", help="The folder/file path for the book", required=True
    )
    parser.add_argument(
        "--print", help="Print output result", required=False, action="store_true"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    logger.info(args)
    test_single_tex_file(args.path, print_result=args.print)
