install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt
run:
	#python3 app.py
	streamlit run app.py
all:
	install run