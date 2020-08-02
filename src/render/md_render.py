#!/usr/bin/python
# -*- coding: UTF-8 -*-
from typing import List
from .constants import ListType, InLineType, IncludeType
import abc
import re


# use (.*) to extract the pattern
# use (?:) to make the extraction optional
# use (.*?) to make a non-greedy match (shortest match)
# use (.*)? to make the match optional
class MDRender():
    def __init__(self, level: int = 0):
        self.level = level
        self.render_line_configs = {
            InLineType.Link: {
                'pattern_str': r"\[(.*?)\]\((.*?)\)",
                'group_num': 2,
            },
            InLineType.Bold: {
                'pattern_str': r"\*\*(.*?)\*\*",
                'group_num': 1,
            },
            InLineType.Include: {
                'pattern_str': r"\{\{(.*?)\}\}\[(.*?)\]",
                'group_num': 2,
            },
        }

    @abc.abstractmethod
    def render_title(self, title, level) -> str:
        pass

    @abc.abstractmethod
    def render_list(self, items: List[str], type_: ListType=ListType.Normal) -> str:
        pass

    @abc.abstractmethod
    def build_inline_link(self, title: str, link: str) -> str:
        pass

    @abc.abstractmethod
    def build_inline_bold(self, content: str) -> str:
        pass

    @abc.abstractmethod
    def build_inline_include(self, content: str, type_: IncludeType) -> str:
        pass

    def build_inline_new_pattern(self, match, inline_type: InLineType) -> str:
        if inline_type == InLineType.Link:
            title = match.group(1)
            link = match.group(2)
            return self.build_inline_link(title, link)
        elif inline_type == InLineType.Bold:
            content = match.group(1)
            return self.build_inline_bold(content)
        elif inline_type == InLineType.Include:
            content = match.group(1)
            setting = match.group(2)
            if len(setting.split(":", 1)) == 2:
                type_ = setting.split(":", 1)[0]
                config = setting.split(":", 1)[1]
            else:
                type_ = setting
                config = ""
            return self.build_inline_include(content, type_, config)
        return ""

    def render_line_with(self, line, inline_type, config) -> str:
        changed = True
        while changed:
            pattern = re.compile(config['pattern_str'], re.IGNORECASE)
            match = pattern.search(line)
            if match and len(match.groups()) == config['group_num']:
                old_pattern = match.group(0)
                new_pattern = self.build_inline_new_pattern(match, inline_type)
                line = line.replace(old_pattern, new_pattern)
            else:
                changed = False
        return line

    @abc.abstractmethod
    def render_line(self, line: str) -> str:
        for inline_type, config in self.render_line_configs.items():
            line = self.render_line_with(line, inline_type, config)
        return line

    @abc.abstractmethod
    def render_blockquote(self, content) -> str:
        pass

    @abc.abstractmethod
    def render_math(self, content) -> str:
        pass

    @abc.abstractmethod
    def render_code(self, content, language) -> str:
        pass
