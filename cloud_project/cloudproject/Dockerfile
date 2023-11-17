FROM python:3.9-slim

WORKDIR /cloudproject

COPY . .

RUN pip install -r requirements.txt

CMD gunicorn --bind 0.0.0.0:5000 new:app
