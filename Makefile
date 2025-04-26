install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt
run:
	python3 -m src.main
all:
	install run