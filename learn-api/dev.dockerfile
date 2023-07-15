FROM python:3.9-slim
ENV PYTHONPATH "${PYTHONPATH}:/app/"

# ARG MYSQL_ROOT_PASSWORD
# ENV MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}

# ARG MYSQL_HOST
# ENV MYSQL_HOST=${MYSQL_HOST}

# ARG MYSQL_DATABASE
# ENV MYSQL_DATABASE=${MYSQL_DATABASE}

RUN apt-get update && apt-get install -y supervisor && apt-get install -y libvips && apt-get install -y default-mysql-client && apt-get install libgeos-dev ffmpeg libsm6 libxext6  -y

COPY supervisord.dev.conf /etc/supervisor/conf.d/supervisord.conf

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY ./alembic /alembic
ADD alembic.ini /

COPY ./app /app
ADD entry.sh /
ENTRYPOINT [ "/entry.sh"]
