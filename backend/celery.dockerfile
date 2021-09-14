FROM python:3-slim
ENV PYTHONPATH "${PYTHONPATH}:/app/"
RUN apt-get update && apt-get install -y libvips
ADD requirements.txt /

RUN pip install -r requirements.txt

RUN mkdir -p /data/slide

COPY ./app /app
ENTRYPOINT celery
CMD ["-A app.worker.tasks worker -c 2 --loglevel=DEBUG --without-gossip --without-mingle --without-heartbeat -Ofair"]
