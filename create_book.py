#!/usr/bin/python
# -*- coding: UTF-8 -*-
from src.render.latex import DOCUMENT, ABSTRACT, SECTION, NEW_LINE
from src.utils.path import read, write, trim_ext
from src.converter import md2tex
from src.constants import LOGGER_FORMAT
from src.config import get_config
from os import listdir
from os.path import isfile, isdir
import markdown
import argparse
import logging
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format=LOGGER_FORMAT)

MAIN_FILE = "MAIN"
INDEX_FILE = "_INDEX"


def get_title(section: str) -> str:
    return trim_ext(section)


def create_by_folder(args) -> str:
    def travel(path: str, level: int = 0) -> str:
        # TODO: refactoring into a class
        content = ""
        sections = listdir(path)

        # Add main content in this section before add sub sections.
        if MAIN_FILE in sections:
            child_path = path + "/" + MAIN_FILE
            if isfile(child_path):
                file_content = md2tex(read(child_path), level + 1)
                content += NEW_LINE([file_content])

        str_sections = []
        sections_titles = []
        for section in sections:
            # ingore this section for now if it's prefix with '_'
            if len(section) > 0 and section[0] in ['_', '.']:
                continue
            child_path = path + "/" + section
            if isfile(child_path) and section != MAIN_FILE:
                file_content = md2tex(read(child_path), level + 1)
                str_sections.append(SECTION(section, file_content, level))
                sections_titles.append(section)
            elif isdir(child_path):
                str_section = NEW_LINE([
                    SECTION(section, "", level),
                    travel(child_path, level=level+1)
                ])
                str_sections.append(str_section)
                sections_titles.append(section)

        # Sort sections by _INDEX file.
        if INDEX_FILE in sections:
            child_path = path + "/" + INDEX_FILE
            titles = read(child_path).split("\n")
            orders = {}
            level = 1
            for title in titles:
                orders[title] = level
                level += 1
            if "*" not in list(orders.keys()):
                orders["*"] = level
            section_levels = [
                orders[title] if title in list(orders.keys()) else orders["*"]
                for title in sections_titles
            ]
            str_sections = [x for _,x in sorted(zip(section_levels, str_sections))]
        else:
            str_sections = sorted(str_sections, key=len, reverse=True)
        content += NEW_LINE(str_sections)
        return content
    return travel(args.path)



def create_by_file(args) -> str:
    content = md2tex(read(args.path), level=args.level)
    return content


def get_args() -> argparse.Namespace:
    logger.info("Parse arguments.")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path", help="The folder/file path for the book", required=True
    )
    parser.add_argument(
        "--bg", help="Background image for the title page", required=False
    )
    parser.add_argument(
        "--simple", help="Output a simple standalone pdf", required=False, action="store_true"
    )
    parser.add_argument(
        "--is_article", help="Output an article rather than a book (ignore title, toc, etc)", required=False, action="store_true"
    )
    parser.add_argument(
        "--level", help="The first level of the book section, default to 0: chapter", default=0, required=False, type=int,
    )
    parser.add_argument(
        "--config", help="The config name of the book", required=False, default='DEFAULT',
    )
    parser.add_argument(
        "--name", help="The name of the book", required=True
    )
    parser.add_argument(
        "--output", help="The output folder for the pdf and log files, default='log'", required=False, default='log',
    )
    parser.add_argument(
        "--author", help="The author of the book", required=False
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    logger.info(args)
    if args.output:
        output = f"{args.output}/{args.name}.tex"
    output_content = ""
    if isdir(args.path):
        output_content = create_by_folder(args)
    elif isfile(args.path):
        output_content = create_by_file(args)

    write(
        output,
        DOCUMENT(
            config=get_config(args.config),
            book_title=args.name,
            content=output_content,
            bg_image=args.bg,
            book_author=args.author,
            is_simple=args.simple,
            is_article=args.is_article,
        )
    )
