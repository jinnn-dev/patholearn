FROM python:3.9-slim
ENV PYTHONPATH "${PYTHONPATH}:/app/"

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 libvips -y

COPY requirements.txt /
COPY requirements.dev.txt /

RUN pip install --upgrade pip
RUN pip install -r requirements.txt -r requirements.dev.txt

COPY ./app /app