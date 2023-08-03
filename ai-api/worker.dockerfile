FROM python:3.11-slim
ENV PYTHONPATH "${PYTHONPATH}:/app/"

RUN apt-get update && apt-get install -y supervisor -y build-essential && apt-get install -y ffmpeg libsm6 libxext6
COPY supervisord.dev.conf /etc/supervisor/conf.d/supervisord.conf

COPY worker.requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./app /app
COPY entry.sh /