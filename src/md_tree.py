#!/usr/bin/python
# -*- coding: UTF-8 -*-
import abc
from .render.md_render import MDRender
from .constants import BlockType
from .render.constants import ListType

# markdown wiki: https://simplemde.com/markdown-guide
# Markdown 解析原理详解和 Markdown AST 描述: https://88250.b3log.org/articles/2020/04/23/1587637426085.html
# Doc -> List[Sections]
# Section = (Title) + (Content)
# Title = Text, Level
# Content = List[Block]
# Block = List[Line], BlockType
# BlockType = Paragraph | List | Quote | Math ｜ Code ｜ Table
# Line (Inline change):
# * 链接（蓝色）
# * 特殊字符，如%
# * 加粗（变红）
# * 斜体（变绿）
# * 划线
# * 分割线
# * 图片：代码画图
# * inline math
# * inline code

# TODO:
# * Support nested List


class Element():
    def __init__(self, text: str, level: int = 0):
        self.text = text
        self.level = level
        self.prefix_tabs = "\t" * level
        self.clear()

    @abc.abstractmethod
    def parse(self):
        pass

    @abc.abstractmethod
    def clear(self):
        pass

    @abc.abstractmethod
    def print(self):
        pass

    @abc.abstractmethod
    def render_with(self, render: MDRender) -> str:
        pass

    def get_text(self):
        return self.text


class Title(Element):
    def __init__(self, text: str, level: int = 0):
        super().__init__(text, level)
        assert len(text) > 0
        assert text[0] == '#'

    def get_title_level(self):
        return self.title_level

    def adjust_title_level(self, delta: int):
        self.title_level += delta

    def clear(self):
        self.title_level = 0
        self.title_text = ""

    def parse(self):
        for c in self.text:
            if c == '#':
                self.title_level += 1
            else:
                break
        self.title_text = self.text[self.title_level:].strip()

    def print(self):
        print(f"{self.prefix_tabs}Title: level: {self.title_level}")
        print(f"{self.prefix_tabs}Title: text: {self.title_text}")

    def render_with(self, render: MDRender) -> str:
        return render.render_title(self.title_text, self.title_level)


class Block(Element):
    def __init__(self, text: str, type_: BlockType, level: int = 0):
        self.type = type_
        super().__init__(text, level)

    def clear(self):
        self.lines = []
        self.setting = ""

    def parse(self):
        self.lines = self.text.split("\n")
        if self.type == BlockType.Quote:
            self.lines = [line[1:].lstrip() for line in self.lines]
        elif self.type == BlockType.List: # For each line, start with space + "* "
            level = 0 # the first level, no extra * needed
            space_num = 0
            step = 4 # default size of tab
            for i in range(0, len(self.lines)):
                line = self.lines[i]
                line_space_num = len(line.split("*", 1)[0])
                if line_space_num > space_num:
                    step = line_space_num - space_num
                    level += 1
                elif line_space_num < space_num:
                    level -= int((space_num-line_space_num) / step)
                    level = level if level >= 0 else 0
                elif line_space_num == space_num:
                    level = level
                space_num = line_space_num
                self.lines[i] = "*" * level + line.lstrip()

            # self.lines = [line[1:].lstrip() for line in self.lines]
        elif self.type == BlockType.NumberList: # For each line, start with "1. ", "2. ", etc.
            self.lines = [line.split(".", 1)[1].lstrip() for line in self.lines]
        elif self.type == BlockType.Math: # start and end with "$$"
            self.lines[0] = self.lines[0].lstrip()
            self.lines[0] = self.lines[0].lstrip("\$")
            self.lines[-1] = self.lines[-1].rstrip()
            self.lines[-1] = self.lines[-1].rstrip("\$")
        elif self.type == BlockType.Code: # start and end with "```"
            self.lines[0] = self.lines[0].lstrip()
            self.lines[0] = self.lines[0].lstrip("`")
            self.setting = self.lines[0]
            self.lines[-1] = self.lines[-1].rstrip()
            self.lines[-1] = self.lines[-1].rstrip("`")

    def print(self):
        print(f"{self.prefix_tabs}Block: number of lines: {len(self.lines)} with type {self.type}")

    def render_with(self, render: MDRender) -> str:
        if self.type == BlockType.Math:
            text = "\n".join(self.lines)
            return render.render_math(text)
        elif self.type == BlockType.Code:
            text = "\n".join(self.lines)
            return render.render_code(text, self.setting)

        lines = [render.render_line(line) for line in self.lines]
        text = "\n".join(lines)
        if self.type == BlockType.Quote:
            return render.render_blockquote(text)
        elif self.type == BlockType.List:
            return render.render_list(lines)
        elif self.type == BlockType.NumberList:
            return render.render_list(lines, type_=ListType.Number)
        else:
            return text


class Content(Element):
    def __init__(self, text: str, level: int = 0):
        super().__init__(text, level)

    def clear(self):
        self.blocks = []

    def parse(self):
        lines = self.text.split("\n")
        start = 0
        end = 0
        block_type = None
        while end < len(lines):
            line = lines[end]
            in_block = True if block_type in [BlockType.Math, BlockType.Code] else False
            # TODO: Refactoring to build automation
            # For Quote '> '
            if len(line) >= 1 and line.startswith(">"):
                if block_type == BlockType.Quote or in_block:
                    pass
                elif end > start:
                    self.blocks.append(Block("\n".join(lines[start:end]), block_type, self.level+1))
                    # print(f"Create Blcok from lines [{start+1}, {end}] with type {block_type}")
                    start = end
                    block_type = BlockType.Quote
                else:
                    block_type = BlockType.Quote
            # For List '* '
            # 2级或多级嵌套List
            elif line.lstrip().startswith("* "):
                if block_type == BlockType.List or in_block:
                    pass
                elif end > start:
                    self.blocks.append(Block("\n".join(lines[start:end]), block_type, self.level+1))
                    # print(f"Create Blcok from lines [{start+1}, {end}] with type {block_type}")
                    start = end
                    block_type = BlockType.List
                else:
                    block_type = BlockType.List
            # For NumberList '1. '
            elif len(line.split(". ")) >= 2 and line.split(". ")[0].isdigit():
                if block_type == BlockType.NumberList or in_block:
                    pass
                elif end > start:
                    self.blocks.append(Block("\n".join(lines[start:end]), block_type, self.level+1))
                    # print(f"Create Blcok from lines [{start+1}, {end}] with type {block_type}")
                    start = end
                    block_type = BlockType.NumberList
                else:
                    block_type = BlockType.NumberList
            # For Math '$$'
            elif len(line) >= 2 and line.startswith("$$"):
                if block_type == BlockType.Math:
                    self.blocks.append(Block("\n".join(lines[start:end+1]), block_type, self.level+1))
                    # print(f"Create Blcok from lines [{start+1}, {end+1}] with type {block_type}")
                    start = end + 1
                    block_type = None
                elif in_block:
                    pass
                elif end > start:
                    self.blocks.append(Block("\n".join(lines[start:end]), block_type, self.level+1))
                    # print(f"Create Blcok from lines [{start+1}, {end}] with type {block_type}")
                    start = end
                    block_type = BlockType.Math
                else:
                    block_type = BlockType.Math
            # For Code '```'
            elif len(line) >= 3 and line.startswith("```"):
                if block_type == BlockType.Code:
                    self.blocks.append(Block("\n".join(lines[start:end+1]), block_type, self.level+1))
                    # print(f"Create Blcok from lines [{start+1}, {end+1}] with type {block_type}")
                    start = end + 1
                    block_type = None
                elif in_block:
                    pass
                elif end > start:
                    self.blocks.append(Block("\n".join(lines[start:end]), block_type, self.level+1))
                    # print(f"Create Blcok from lines [{start+1}, {end}] with type {block_type}")
                    start = end
                    block_type = BlockType.Code
                else:
                    block_type = BlockType.Code
            # For Normal text, etc
            else:
                if block_type in [BlockType.Text, BlockType.Math, BlockType.Code]:
                    pass
                elif end > start:
                    self.blocks.append(Block("\n".join(lines[start:end]), block_type, self.level+1))
                    # print(f"Create Blcok from lines [{start+1}, {end}] with type {block_type}")
                    start = end
                    block_type = BlockType.Text
                else:
                    block_type = BlockType.Text
            end += 1

        if end > start:
            self.blocks.append(Block("\n".join(lines[start:end]), block_type, self.level+1))
            # print(f"Create Blcok from lines [{start+1}, {end}] with type {block_type}")

        for block in self.blocks:
            block.parse()

    def print(self):
        print(f"{self.prefix_tabs}Content: number of blocks: {len(self.blocks)}")
        for block in self.blocks:
            block.print()

    def render_with(self, render: MDRender) -> str:
        blocks = []
        for block in self.blocks:
            blocks.append(block.render_with(render))
        return "\n".join(blocks)


class Section(Element):
    def __init__(self, text: str, level: int = 0):
        super().__init__(text, level)

    def get_title_level(self):
        if self.title:
            return self.title.get_title_level()
        else:
            return 0

    def adjust_title_level(self, delta: int):
        if self.title:
            return self.title.adjust_title_level(delta)

    def clear(self):
        self.title = None
        self.content = None

    def parse(self):
        if len(self.text) > 0:
            if self.text[0] == "#":  # This is a section with title
                parts = self.text.split("\n", 1)
                self.title = Title(parts[0], self.level+1)
                if len(parts) > 1:
                    self.content = Content(parts[1], self.level+1)
            else:
                self.content = Content(self.text, self.level+1)

        if self.title:
            self.title.parse()
        if self.content:
            self.content.parse()

    def print(self):
        title = self.title.get_text() if self.title else "None"
        print(f"{self.prefix_tabs}Section: title: {title}")
        content_len = len(self.content.get_text()) if self.content else 0
        print(f"{self.prefix_tabs}Section: len of content: {content_len}")
        if self.title:
            self.title.print()
        if self.content:
            self.content.print()

    def render_with(self, render: MDRender) -> str:
        result = ""
        if self.title:
            result += self.title.render_with(render) + "\n"
        if self.content:
            result += self.content.render_with(render)
        return result


class MDDocument(Element):
    # level = 本文档内首层目录级别，0=Chapter
    def __init__(self, text: str, level: int = 0):
        super().__init__(text, level)

    def clear(self):
        self.sections = []

    def parse(self):
        has_main = True # has main text before the first title section
        if self.text.startswith("#"):
            has_main = False

        raw_sections = self.text.split("\n#")
        self.sections.append(Section(raw_sections[0], self.level))
        for raw_section in raw_sections[1:]:
            raw_section = "#" + raw_section
            self.sections.append(Section(raw_section, self.level))
        for section in self.sections:
            section.parse()

        # adjust title level so the top title level = self.level
        title_levels = [section.get_title_level() for section in self.sections]
        if has_main:
            title_levels = title_levels[1:]

        if len(title_levels) > 0:
            top_title_level = min(title_levels)
            if has_main is False:
                self.sections[0].adjust_title_level(- top_title_level + self.level)
            for section in self.sections[1:]:
                section.adjust_title_level(- top_title_level + self.level)

    def print(self):
        print(f"{self.prefix_tabs}MDDocument: number of sections: {len(self.sections)}")
        for section in self.sections:
            section.print()

    def render_with(self, render: MDRender) -> str:
        sections = []
        for section in self.sections:
            sections.append(section.render_with(render))
        return "\n".join(sections)
