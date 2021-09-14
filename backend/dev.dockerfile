FROM python:3.9-slim
ENV PYTHONPATH "${PYTHONPATH}:/app/"

RUN apt-get update && apt-get install -y supervisor && apt-get install -y libvips && apt-get install -y default-libmysqlclient-dev && apt-get install -y default-mysql-client
COPY supervisord.dev.conf /etc/supervisor/conf.d/supervisord.dev.conf

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY ./app /app
#ADD entry.sh /
#CMD /entry.sh
