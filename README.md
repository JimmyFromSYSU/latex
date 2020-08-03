
## 概述


通过运行以下命令，可以将本Markdown文档生成pdf格式，建议阅读pdf版本的README。

```
make readme
```

本工具用于个人辅助写作和作图等，满足各种文档编辑的需求。

* 该系统写作部分以基本的Markdown语法为核心，作图部分使用Latex和dot等通用工具包。
* 该系统会生成Markdown语法树，可通过Latex渲染生成pdf等，也可以通其他渲染方式生成Html，Word等格式，方便发布文章。
* 该系统支持将批量的Markdown文档整理成册，比如合成一本书，并设置封面和章节目录等。
* 该系统可以通过pgfplot，tikz等工具，快速制作复杂的数学图片。


### 处理单个文档
本系统可以将一个Markdown文档转化为tex文档，并自动生成封面和目录，后续还通过latex工具包转化为pdf。只需要将文档路径传入path。

```
python3 create_book.py --path README.md --name README --author 南方小智
@echo 'xelatex cmd support Chinese'
xelatex -output-directory log README.tex
@echo 'run twice to build toc correctly'
xelatex -output-directory log README.tex
```

* name代表生成的文件名和封面标题。
* author代表生成的封面作者。
* 生成的tex文件在log文件夹中。

### 处理多个文档
本系统可以将多个Markdown文档合成一个tex文档，并自动生成封面和目录，后续还通过latex工具包转化为pdf。只需要将所有文档放在同一个文件夹里，并将文件夹路径传入path。


```
python3 create_book.py --path examples/趣题集/ --name 趣题集 --bg images/趣题集/background.jpeg --author 南方小智
@echo 'xelatex cmd support Chinese'
xelatex -output-directory log 趣题集.tex
@echo 'run twice to build toc correctly'
xelatex -output-directory log 趣题集.tex
```

* 支持多层文件夹，每层文件夹对应一个目录级别，比如文件夹内第一层目录每个文件夹名字为每章的名字，第二层目录每个文件夹名字为每节的名字。
* MAIN文件为保留文件名，为该层目录对应章节的导言部分。
* \_INDEX文件为保留文件名，用于对文件夹（章节）进行排序，目前章节的排列方法是较长的章节放在靠前的位置。
* 名字以“\_”开始的文件夹或者文件会被忽略。

\_INDEX文件中按顺序列举该层目录的标题，未列举的标题将放在“\*”的位置。如果“\*”未标注在文件中，则未列举的标题默认排到最后。

{{examples/趣题集/_INDEX}}[code]


### 生成图片文件
本系统可以编译单一tex文档，并生成图片。只需要使用simple参数，就可以省略标题，目录，页码等，生成一个独立的图片形式，后续可以用convert命令将pdf转为图片。

```
python3 create_book.py --path images/趣题集/三角形悖论/image0.tex --name 三角形 --simple
xelatex -output-directory log 三角形.tex
@echo '需要安装brew install imagemagick'
convert -density 300 log/三角形.pdf -quality 90 log/三角形.png
```

### 所有测试用例
```
make readme     # 将本文档生成pdf
make all        # 生成一本《趣题集》
make image      # 生成一张png图片 (需要安装brew install imagemagick)
make clean      # 清空log文件
make clean_all  # 清空所有生成文件，包括，log文件，tex文件， pdf文件等
```

具体细节请参照makefile：

{{makefile}}[code:Bash]

## Markdown支持

基本语法请参照：[markdown wiki](https://simplemde.com/markdown-guide)

### 特殊字符

在Markdown文件中使用特殊字符时需要进行特殊处理，比如添加转义字符\\
```
_ -> \_   # _ 在Markdown中可用于表示斜体
* -> \*   # * 在Markdown中可用于表示斜体
$ -> \$   # $ 在Markdown中可用于开始数学表达式模式
\ -> \\   # \ 是特殊的Latex符号
```

### 导入代码文件

```
{{create_book.py}}[code:Python] # 导入代码文件
```

{{create_book.py}}[code:Python]

### 导入tex格式的图片文件

```
{{images/趣题集/三角形悖论/image1.tex}}[image] # 导入tex格式的图片文件
```

{{images/趣题集/三角形悖论/image1.tex}}[image]

### Markdown转化器
该系统自带一个Markdown解析器，会将Markdown文本转化为一棵语法树。使用如下命令可以打印出本Readme文档的语法树：

```
make test  # python3 test.py --path README.md
```

通过渲染器，可以将Markdown渲染成tex，html，word等格式。只需要继承MDRender，实现对应的抽象方法即可添加新的渲染器，比如src/render/md\_tex\_render.py。

{{src/render/md_render.py}}[code:Python]


## TODO

* 目前很多latex设置都是Hard Code的，应当将这些设置变成可配置的：
    * 目前目录最多显示两层标题结构
    * 目前最高层目录默认为Chapter，设置level参数使其可配置化
* 目前Markdown解析器仍然有许多Markdown基本语法并不支持，需要：
    * 支持行内斜体，下划线等。
    * 支持行内代码。
    * 支持一般图片格式的导入
    * [Done] 支持嵌套List
        * 测试3层嵌套
    * 支持表格
* 目前Latex渲染器仍然有一些Latex用法支持不够，需要：
    * 支持更多类似\$，<，>等latex特殊字符。
* 支持更多的Features：
    * 添加页面背景水印，这样可以防止发布的材料被盗版使用。
    * 添加程序辅助画图（特别是制作复杂的各类数学图片）。
    * 添加作者介绍。
    * 添加html和word渲染器。
* Better Engineering：
    * md\_tree的Parser主体可以用自动机的方式实现，从而减少if/else的判断和重复代码片。
