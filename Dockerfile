FROM python:3.10

ENV PYTHONBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn","newsapp.wsgi","--bind","0.0.0.0:8080"]