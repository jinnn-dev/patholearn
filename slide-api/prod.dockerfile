FROM python:3.9-slim
ENV PYTHONPATH "${PYTHONPATH}:/app/"

RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 && apt-get install -y imagemagick && apt-get install -y libvips

COPY requirements.txt /
RUN mkdir -p /data
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./app /app
