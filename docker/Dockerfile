FROM python:3.8-slim

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
ENV PYTHONUNBUFFERED=0
CMD python3 -u main.py
