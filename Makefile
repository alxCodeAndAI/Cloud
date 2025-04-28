install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt
run:
	#python3 app.py
	streamlit run app.py --server.address=0.0.0.0 --server.port=8501
all:
	install run