#!/usr/bin/python
# -*- coding: UTF-8 -*-
from src.render.latex import DOCUMENT, ABSTRACT, SECTION, NEW_LINE
from src.utils.path import get_sections, read, write
from src.converter import md2tex
from src.constants import LOGGER_FORMAT
from os import listdir
from os.path import isfile, isdir
import markdown
import argparse
import logging
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format=LOGGER_FORMAT)

MAIN_FILE = "MAIN"

def create_by_folder(args) -> str:
    def travel(path: str, level: int = 0) -> str:
        # TODO: refactoring into a class
        content = ""
        sections = get_sections(path)
        sections.sort()

        # Add main content in this section before add sub sections.
        if MAIN_FILE in sections:
            child_path = path + "/" + MAIN_FILE
            if isfile(child_path):
                file_content = md2tex(read(child_path), level + 1)
                content += NEW_LINE([file_content])

        str_sections = []
        for section in sections:
            # ingore this section for now if it's prefix with '_'
            if len(section) > 0 and section[0] in ['_', '.']:
                continue
            child_path = path + "/" + section
            if isfile(child_path) and section != MAIN_FILE:
                file_content = md2tex(read(child_path), level + 1)
                str_sections.append(SECTION(section, file_content, level))
            elif isdir(child_path):
                str_section = NEW_LINE([
                    SECTION(section, "", level),
                    travel(child_path, level=level+1)
                ])
                str_sections.append(str_section)
        str_sections = sorted(str_sections, key=len, reverse=True)
        content += NEW_LINE(str_sections)
        return content
    return travel(args.path)



def create_by_file(args) -> str:
    content = md2tex(read(args.path), level=0)
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
        "--name", help="The name of the book", required=True
    )
    parser.add_argument(
        "--author", help="The author of the book", required=False
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    logger.info(args)

    output = f"log/{args.name}.tex"
    output_content = ""
    if isdir(args.path):
        output_content = create_by_folder(args)
    elif isfile(args.path):
        output_content = create_by_file(args)

    write(
        output,
        DOCUMENT(
            args.name,
            output_content,
            bg_image=args.bg,
            book_author=args.author,
            is_simple=args.simple,
        )
    )
