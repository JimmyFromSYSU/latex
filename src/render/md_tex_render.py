#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .latex import SECTION_TITLE, BLOCK_QUOTE, LIST, NUMBER_LIST, BLOCK_MATH, BLOCK_CODE
from typing import List
from .constants import ListType, IncludeType, DOT_IMAGE_TYPE
from .md_render import MDRender
import os

from ..constants import LOGGER_FORMAT
import logging
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format=LOGGER_FORMAT)


# TODO: move to md_render, now it's only used by latex render
class ListNode():
    def __init__(self, lines: List[str], level: int = 0, head_line=""):
        start = 0
        end = 0

        self.head_line = head_line.lstrip("*").lstrip()
        self.level = level
        self.is_leaf = False
        self.nodes = []

        if len(lines) == 0:
            self.is_leaf = True
            return

        self.nodes = []
        while end < len(lines):
            line = lines[end]
            line_level = len(line.split(' ', 1)[0])
            if line_level <= self.level + 1:
                if end > start:
                    self.nodes.append(ListNode(lines=lines[start+1:end], level=self.level+1, head_line=lines[start]))
                    start = end
            end += 1
        if end > start:
            self.nodes.append(ListNode(lines=lines[start+1:end], level=self.level+1, head_line=lines[start]))

    def render(self, type_: ListType=ListType.Normal) -> str:
        if self.is_leaf:
            return self.head_line
        items = [node.render() for node in self.nodes]
        return self.head_line + "\n" + LIST(items)


class MDTexRender(MDRender):
    def __init__(self, level: int = 0):
        super().__init__(level)

    def render_title(self, title, level) -> str:
        return SECTION_TITLE(self.render_line(title), self.level + level)

    def build_inline_link(self, title: str, link: str) -> str:
        return f"\\href{{{link}}}{{{title}}}"

    def build_inline_image(self, title: str, link: str) -> str:
        # width=\linewidth
        # [H]取消图片默认置顶: https://blog.csdn.net/ymjiang820/article/details/50474586
        begin = r"\begin{center}\begin{figure}[H] \centering \includegraphics[max size={\textwidth}{\textheight},keepaspectratio]"
        content = f"{{{link}}}\\caption*{{{title}}}"  # use * to remove label.
        end = r"\end{figure} \end{center}"
        return f"{begin}\n{content}\n{end}"

    def build_inline_bold(self, content: str) -> str:
        return f"\\textbf{{\\textcolor{{Firebrick}}{{{content}}}}}"

    def build_inline_include(self, path: str, type_: IncludeType, config: str="") -> str:
        if type_ == IncludeType.Image:
            begin = r"\begin{center}"
            end = r"\end{center}"
            return f"{begin}\n\\input{{{path}}}\n{end}"
        elif type_ == IncludeType.Dot:
            img_path = f"{path}.{DOT_IMAGE_TYPE}"
            cmd = f"dot -Teps {path} > {img_path}"

            logger.info(f"Creating eps image file for {path}")
            logger.info(f"cmd: {cmd}")

            stream = os.popen(cmd)
            output = stream.read()
            logger.info(f"Result: {output.strip()}")

            title = config
            return self.build_inline_image(title, img_path)
        elif type_ == IncludeType.Code:
            return f"\\lstinputlisting[language={config}]{{{path}}}"
        else:
            return f"\\input{{{path}}}"

    def render_list(self, items: List[str], type_: ListType=ListType.Normal) -> str:
        if type_ == ListType.Number:
            return NUMBER_LIST(items)
        else:
            root = ListNode(items)
            return root.render(type_=ListType.Normal)
            # return LIST(items)

    def render_line(self, line: str) -> str:
        line = line.replace("%", r"\%")
        line = line.replace(r"\*", "*")
        line = line.replace("#", r"\#")
        line = line.replace("&", r"\&")
        line = line.replace(">", r"$>$")
        line = line.replace("<", r"$<$")
        line = line.replace("≈", r"$\approx$")
        line = line.replace("~", r"$\~{}$")
        line = line.replace("\\\\", r"$\backslash$")
        line = super().render_line(line)
        return line

    def render_blockquote(self, content) -> str:
        return BLOCK_QUOTE(content)

    def render_math(self, content) -> str:
        return BLOCK_MATH(content)

    def render_code(self, content, language) -> str:
        return BLOCK_CODE(content, language)
