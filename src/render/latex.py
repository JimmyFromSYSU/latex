#!/usr/bin/python
# -*- coding: UTF-8 -*-
from typing import List, Optional


CLEAR_PAGE = "\\clearpage\n"
NEW_PAGE ="\\newpage"
EMPTY_THIS_PAGE = "\\thispagestyle{empty}"
EMPTY_PAGE = "\\pagestyle{empty}"

# http://www.emerson.emory.edu/services/latex/latex_129.html
PLAIN_THIS_PAGE = "\\thispagestyle{plain}"
PLAIN_PAGE = "\\pagestyle{plain}"

# FONT SIZE:
# https://texblog.org/2012/08/29/changing-the-font-size-in-latex/
# \showsize\tiny
# \showsize\scriptsize
# \showsize\footnotesize
# \showsize\small
# \showsize\normalsize
# \showsize\large
# \showsize\fourteenpt
# \showsize\Large
# \showsize\LARGE
# \showsize\huge
# \showsize\Huge

def DOC_OPTIONS(
    main_font: str = "12pt",
    paper_size: str = "letterpaper", # a4paper, a5paper, b5paper, executivepaper, and legalpaper
) -> str:
    # export: https://ipfs-sec.stackexchange.cloudflare-ipfs.com/tex/A/question/263869.html
    items = ["export"]
    if main_font:
        items.append(main_font)
    if paper_size:
        items.append(paper_size)
    if len(items):
        return f"[{', '.join(items)}]"
    else:
        return ""


def TRIM_STRING_BLOCK(input: str) -> str:
    return "\n".join([line.lstrip() for line in input.split("\n")])


def NEW_LINE(parts: List[str]) -> str:
    return "\n".join(parts) + "\n"


COMMON_SETTINGS = r"""
\usepackage{titling}
\usepackage{standalone}
\usepackage{fontenc}
"""

# TODO: add USE_PAKAGE function
# \part and \chapter are only available in report and book document classes.
# -1 \part{part}
# 0	\chapter{chapter}
# 1	\section{section}
# 2	\subsection{subsection}
# 3	\subsubsection{subsubsection}
# 4	\paragraph{paragraph}
# 5	\subparagraph{subparagraph}
TOC_SETTINGS = r"""
\usepackage{hyperref}
\hypersetup{
    colorlinks=true,
    linkcolor=DarkBlue,
    urlcolor=blue,
    linktoc=all
}
\setcounter{tocdepth}{1}
"""

PADDING_SETTINGS = """
\\usepackage[
    left=1.0in,
    right=1.0in,
    top=1.5in,
    bottom=1.5in,
]{geometry}
"""


# math background color: https://tex.stackexchange.com/questions/75129/boxed-tikz-and-colored-equation-background
# \\usepackage{amsmath}
# https://en.wikibooks.org/wiki/LaTeX/Mathematics
MATH_SETTINGS = r"""
\usepackage{mathtools}
\usepackage{amsmath}
\usepackage{tikz}
\usepackage{verbatim}
\usetikzlibrary{calc}

% put color to \boxed math command
\newcommand*{\boxcolor}{Peru}
\makeatletter
\renewcommand{\boxed}[1]{\textcolor{\boxcolor}{%
\tikz[baseline={([yshift=-1ex]current bounding box.center)}] \node [rectangle, minimum width=1ex,rounded corners,draw] {\normalcolor\m@th$\displaystyle#1$};}}
\makeatother
"""

# \usetikzlibrary[petri] % ConTEXt
PGF_SETTINGS = r"""
\usetikzlibrary{positioning}
\usetikzlibrary{petri} % LATEX and plain TEX
\usetikzlibrary[petri] % ConTEXt
\usepackage{pgfplots}
\pgfplotsset{compat=1.13}
"""


# COLOR
# https://www.cnblogs.com/tsingke/p/7457236.html
# \textcolor{red/blue/green/black/white/cyan/magenta/yellow}{text}
#
# 组合red、green和blue的值合成我们想要的颜色
# \usepackage{color}
# \textcolor[rgb]{r,g,b}{text}
# 其中{r,g,b}代表red、green和blue三种颜色的组合，取值范围为[0-1]
# \textcolor[RGB]{R,G,B}{text}
#
# 定义一种颜色，直接调用
# \usepackage{color}
# \definecolor{ColorName}{rgb}{r,g,b}      这时r/g/b的定义域就在[0-1]。
#\definecolor{ColorName}{RGB}{R,G,B}，这时R/G/B的定义域就在[0-255]。
# 这里为颜色定义了名称ColorName，下面可以直接调用这个颜色方案
# \textcolor{ColorName}{text}
# 其中{R,G,B}代表red、green和blue三种颜色的组合，取值范围为[0-255]
# Table of Color: https://www.farb-tabelle.de/en/table-of-color.htm



# wiki: https://en.wikibooks.org/wiki/LaTeX/Colors
# \usepackage[dvipsnames]{xcolor}: https://www.overleaf.com/learn/latex/Using_colours_in_LaTeX#Reference_guide
# \usepackage[x11names]{xcolor}: https://www.farb-tabelle.de/en/table-of-color.htm
# \textcolor{red/blue/green/black/white/cyan/magenta/yellow}{text}
# \usepackage{color}
# definecolor color comes from https://en.wikipedia.org/wiki/X11_color_names
COLOR_SETTINGS = r"""
\usepackage[x11names]{xcolor}
\definecolor{SaddleBrown}{rgb}{0.55, 0.27, 0.07}
\definecolor{IndianRed}{rgb}{0.80, 0.36, 0.36}
\definecolor{Firebrick}{rgb}{0.70, 0.13, 0.13}
\definecolor{DarkBlue}{rgb}{0, 0, 0.55}
\definecolor{Goldenrod}{rgb}{0.85, 0.65, 0.13}
\definecolor{Peru}{rgb}{0.85, 0.65, 0.13}
"""

CHINESE_SETTINGS = r"""
\usepackage{ctex}
\usepackage{xeCJK}
\xeCJKsetup{CJKmath=true}
"""

FONT_SETTINGS = """
"""

# TODO: make this configerable
# inlcuding title background image:
# https://tex.stackexchange.com/questions/46280/how-to-create-a-background-image-on-title-page-with-latex
# Set title shift:
# https://tex.stackexchange.com/questions/29593/shift-title-and-author-text-up
def TITLE_SETTINGS(book_title: str, author: Optional[str], bg_image: Optional[str]) -> str:
    if bg_image:
        bg_image_settings = f"""
            \\usepackage{{eso-pic}}
            \\newcommand\\BackgroundPic{{%
            \\put(0,0){{%
            \\parbox[b][\\paperheight]{{\\paperwidth}}{{%
            \\vfill
            \\centering
            \\includegraphics[width=\\paperwidth,height=\\paperheight,%
            keepaspectratio]{{{bg_image}}}%
            \\vfill
            }}}}}}
        """
    else:
        bg_image_settings = ""

    author = author if author else ""

    return TRIM_STRING_BLOCK(
        f"""
        \\setlength{{\\droptitle}}{{-18em}}
        \\title{{\\fontsize{{40}}{{20}} \\textbf{{\\textcolor{{red}}{{\kaishu {book_title}}}}}}}
        \\author{{\\textcolor{{red}}{{{author}}}}}
        \\date{{\\textcolor{{red}}{{\\today}}}}
        {bg_image_settings}
        """
    )

CODE_SETTINGS = r"""
\usepackage{listings}

\definecolor{codegreen}{rgb}{0,0.6,0}
\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\definecolor{codepurple}{rgb}{0.58,0,0.82}
\definecolor{backcolour}{rgb}{0.95,0.95,0.92}

\lstdefinestyle{mystyle}{
    backgroundcolor=\color{backcolour},
    commentstyle=\color{codegreen},
    keywordstyle=\color{magenta},
    numberstyle=\tiny\color{codegray},
    stringstyle=\color{codepurple},
    basicstyle=\ttfamily\footnotesize,
    breakatwhitespace=false,
    breaklines=true,
    captionpos=b,
    keepspaces=true,
    numbers=left,
    numbersep=5pt,
    showspaces=false,
    showstringspaces=false,
    showtabs=false,
    tabsize=2
}

\lstset{style=mystyle}
"""

# https://tex.stackexchange.com/questions/435630/what-is-the-simplest-most-canonical-way-to-change-the-background-color-of-quote
# Table of Color: https://www.farb-tabelle.de/en/table-of-color.htm
# * Blue: LightCyan1, LightSteelBlue1, LightBlue1
# * Pink: LavenderBlush2
BLOCK_QUOTE_SETTINGS = r"""
\usepackage{framed}
\usepackage{quoting}

\colorlet{shadecolor}{LightSteelBlue1}
\usepackage{lipsum}
\newenvironment{shadedquotation}
 {\begin{shaded*}
  \quoting[leftmargin=5pt, rightmargin=5pt, vskip=0pt]
 }
 {\endquoting
 \end{shaded*}
}
"""

LIST_SETTINGS = r"""
\usepackage{lipsum} % for dummy text
\usepackage{enumitem}
\setlist{nosep} % or \setlist{noitemsep} to leave space around whole list
"""

# 去除图片标题中的前缀，如Fig.1: https://tex.stackexchange.com/questions/21795/how-to-remove-figure-label
# float(取消图片默认置顶): https://blog.csdn.net/ymjiang820/article/details/50474586
IMAGE_SETTINGS = r"""
\usepackage{graphicx}
\usepackage{adjustbox}
\usepackage{caption}
\usepackage{float}
"""

# ADD background image
# The * will make sure that the background picture will only be put on one page.
# If you wish to use the picture on multiple pages, skip the *:
# \AddToShipoutPicture{\BackgroundPic}
# Then use this command to stop using the background picture:
# \ClearShipoutPicture
ADD_BG_IMAGE = "\\AddToShipoutPicture*{\\BackgroundPic}"

DOC_TYPES = {
    "article": {
        "chinese_type": "ctexart",
    },
    "book": {
        "chinese_type": "ctexbook",
    },
    "report": {
        "chinese_type": "ctexrep",
    },
    "beamer": {
        "chinese_type": "ctexbeamer",
    },
}


def DOCUMENT(
    book_title: str = "",
    content: str = "",
    options: str = DOC_OPTIONS(),
    is_chinese: bool = True,
    is_simple: bool = False,
    is_article: bool = False,
    bg_image: Optional[str] = None,
    book_author: Optional[str] = None,
    doc_type: str = "report"  # "article", "book", etc
) -> str:
    settings = []

    settings.append(COMMON_SETTINGS)
    settings.append(COLOR_SETTINGS)
    settings.append(FONT_SETTINGS)
    settings.append(TOC_SETTINGS)
    settings.append(MATH_SETTINGS)
    settings.append(CODE_SETTINGS)
    settings.append(PGF_SETTINGS)
    settings.append(BLOCK_QUOTE_SETTINGS)
    settings.append(LIST_SETTINGS)
    settings.append(IMAGE_SETTINGS)
    settings.append(PLAIN_PAGE)

    if is_chinese:
        assert(doc_type in list(DOC_TYPES.keys()))
        type_ = DOC_TYPES[doc_type]["chinese_type"]
        settings.append(CHINESE_SETTINGS)
    else:
        type_ = doc_type

    counter = EMPTY_PAGE
    title = ""
    toc = ""

    if is_simple:
        type_ = "standalone"
    elif is_article:
        settings.append(PADDING_SETTINGS)
    else:
        counter = "\\setcounter{page}{1}"
        title = NEW_LINE(
            [
                ADD_BG_IMAGE if bg_image else "",
                "\\maketitle",
                EMPTY_THIS_PAGE,
                NEW_PAGE,
            ]
        )
        toc = NEW_LINE(
            [
                "\\tableofcontents",
                NEW_PAGE,
            ]
        )
        settings.append(PADDING_SETTINGS)
        settings.append(TITLE_SETTINGS(book_title, book_author, bg_image))

    settings_str = NEW_LINE(settings)

    header = f"\\documentclass{options}{{{type_}}}"
    begin = "\\begin{document}"
    end = "\\end{document}"
    return NEW_LINE(
        [
            header,
            settings_str,
            begin,
            title,
            counter,
            toc,
            content,
            end,
        ]
    )


def BLOCK_QUOTE(content: str) -> str:
    # TODO: quote or shadedquotation? matcht he QUOTE SETTINGS
    begin = r"\begin{shadedquotation}"
    noindent = r"\noindent"
    content = content.replace("\n", f"\n{noindent}\n")
    end = r"\end{shadedquotation}"
    return NEW_LINE(
        [
            begin,
            noindent,
            content,
            end,
        ]
    )

# \part and \chapter are only available in report and book document classes.
# -1 \part{part}
# 0	\chapter{chapter}
# 1	\section{section}
# 2	\subsection{subsection}
# 3	\subsubsection{subsubsection}
# 4	\paragraph{paragraph}
# 5	\subparagraph{subparagraph}
def SECTION_TITLE(title: str, level = 1) -> str:
    section = ""
    if level == -1:
        section = "\\part"
    elif level == 0:
        section = "\\chapter"
    elif level >= 1 and level <= 3:
        prefix = "sub" * (level - 1)
        section = f"\\{prefix}section"
    return f"{section}{{{title}}}"


def SECTION(title: str, content: str = "", level=1) -> str:
    return NEW_LINE(
        [
            f"{SECTION_TITLE(title, level)}",
            content,
        ]
    )


def ABSTRACT(content: str = "") -> str:
    begin = "\\begin{abstract}"
    end = "\\end{abstract}"
    return NEW_LINE(
        [
            begin,
            content,
            end,
            NEW_PAGE,
        ]
    )


def LIST(items: List[str]) -> str:
    begin = r"\begin{itemize}"
    end = r"\end{itemize}"
    prefix = r"\item{"
    suffix = r"}"
    lines = [f"{prefix} {item} {suffix}" for item in items]
    lines.insert(0, begin)
    lines.append(end)
    return NEW_LINE(lines)


def NUMBER_LIST(items: List[str]) -> str:
    begin = r"\begin{enumerate}"
    end = r"\end{enumerate}"
    prefix = r"\item{"
    suffix = r"}"
    lines = [f"{prefix} {item} {suffix}" for item in items]
    lines.insert(0, begin)
    lines.append(end)
    return NEW_LINE(lines)


def BLOCK_MATH(content: str) -> str:
    # begin = "$$\n\\tikzmarkin{a}(0.2,-0.5)(-0.2,0.65)"
    # end = "\\tikzmarkend{a}\n$$"
    begin = "$$\\boxed{"
    end = "}$$"
    return begin + content + end


def BLOCK_CODE(content: str, language: str) -> str:
    language = language if language else "Bash"
    begin = f"\\begin{{lstlisting}}[language={language}]"
    end = r"\end{lstlisting}"
    return begin + content + end
