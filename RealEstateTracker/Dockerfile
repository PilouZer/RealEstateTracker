FROM python:3.8.6-buster

COPY Web/model.joblib Web/model.joblib
COPY RealEstateTracker/utils.py RealEstateTracker/utils.py
COPY Web/streamlite/pages Web/streamlite/pages
COPY Web/streamlite/Intro.py Web/streamlite/Intro.py
COPY Web/app.py Web/app.py
COPY Web/dashboard.py Web/dashboard.py
COPY Web/map.py Web/map.py
COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD streamlit run Web/streamlite/Intro.py  --server.port 8501
