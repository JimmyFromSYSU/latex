#!/usr/bin/python
# -*- coding: UTF-8 -*-
from enum import Enum
from typing import Dict

PADDING_SETTINGS = 'PADDING_SETTINGS'
MAIN_FONT = 'MAIN_FONT'

# https://www.overleaf.com/learn/latex/sections_and_chapters
SECTION_SETTINGS = 'SECTION_SETTINGS'


class CONFIG_NAME(Enum):
    DEFAULT = 'DEFAULT',
    RAW_PAGE = 'RAW_PAGE',


SETTING_CONFIGS = {
    CONFIG_NAME.DEFAULT.name: {
        MAIN_FONT: '12pt',
        PADDING_SETTINGS: r"""
            \usepackage[
                left=1.0in,
                right=1.0in,
                top=1.5in,
                bottom=1.5in,
            ]{geometry}
        """,
        SECTION_SETTINGS: r"""
        """,
    },
    CONFIG_NAME.RAW_PAGE.name: {
        MAIN_FONT: '10pt',
        PADDING_SETTINGS: r"""
            \usepackage[
                left=0.5in,
                right=0.5in,
                top=0.5in,
                bottom=0.5in,
            ]{geometry}
        """,
        SECTION_SETTINGS: r"""
            \usepackage{titlesec}
            \titleformat{\section}[display]{\bfseries\LARGE\itshape}{}{0pt}{}
            \titleformat{\subsection}[display]{\bfseries\Large\itshape}{}{0pt}{}
        """,
    }
}


def get_config(name: CONFIG_NAME) -> Dict[str, str]:
    config = SETTING_CONFIGS[name]
    if name == CONFIG_NAME.DEFAULT.name:
        return config

    default_config = SETTING_CONFIGS[CONFIG_NAME.DEFAULT.name]
    for key, value in default_config.items():
        if key not in config:
            config[key] = value
    return config
