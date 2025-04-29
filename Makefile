venv:
	source .venv/bin/activate &&\
install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt
run:
	streamlit run app.py --server.port=8501
all:
	install run