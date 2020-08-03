all:
	python3 create_book.py --path examples/趣题集/ --name 趣题集 --bg images/趣题集/background.jpeg --author 南方小智
	@echo 'xelatex cmd support Chinese'
	xelatex -output-directory log 趣题集.tex
	@echo 'run twice to build toc correctly'
	xelatex -output-directory log 趣题集.tex
	open log/趣题集.pdf

readme:
	python3 create_book.py --path README.md --name README --author 南方小智
	@echo 'xelatex cmd support Chinese'
	xelatex -output-directory log README.tex
	@echo 'run twice to build toc correctly'
	xelatex -output-directory log README.tex
	open log/README.pdf

image:
	python3 create_book.py --path images/趣题集/三角形悖论/image0.tex --name 三角形 --simple
	xelatex -output-directory log 三角形.tex
	@echo '需要安装brew install imagemagick'
	convert -density 300 log/三角形.pdf -quality 90 log/三角形.png
	open log/三角形.png

test:
	python3 test.py --path README.md

temp:
	python3 create_book.py --path books/棋牌类游戏AI引擎实现/ --name 棋牌类游戏AI引擎实现 --author 南方小智 --output ignore
	@echo 'xelatex cmd support Chinese'
	xelatex -output-directory ignore 棋牌类游戏AI引擎实现.tex
	@echo 'run twice to build toc correctly'
	xelatex -output-directory ignore 棋牌类游戏AI引擎实现.tex
	open ignore/棋牌类游戏AI引擎实现.pdf

clean:
	rm -f log/*.aux
	rm -f log/*.toc
	rm -f log/*.log
	rm -f log/*.out

clean_all:
	rm -f log/*.aux
	rm -f log/*.toc
	rm -f log/*.log
	rm -f log/*.out
	rm -f log/*.tex
	rm -f log/*.png
	rm -f log/*.pdf
