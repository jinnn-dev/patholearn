FROM python:3.9-slim
ENV PYTHONPATH "${PYTHONPATH}:/app/"
RUN apt-get update && apt-get install -y libvips


RUN pip install --upgrade pip
COPY requirements.txt /
RUN pip install -r requirements.txt

COPY ./app /app
