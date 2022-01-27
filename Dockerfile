FROM python:3.10

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
COPY utils.py .
COPY data/apache_logs.txt .

CMD gunicorn app:app -b 0.0.0.0:80