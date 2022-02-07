FROM python:3.9-slim
ENV PYTHONPATH "${PYTHONPATH}:/app/"

RUN apt-get update && apt-get install -y libvips

COPY requirements.txt /
COPY dev.requirements.txt /

RUN pip install --upgrade pip
RUN pip install -r requirements.txt -r requirements.dev.txt

COPY ./app /app