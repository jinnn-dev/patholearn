FROM python:3.9-slim
ENV PYTHONPATH "${PYTHONPATH}:/app/"
<<<<<<< HEAD:pyramid-creator/Dockerfile
RUN apt-get update && apt-get install -y imagemagick && apt-get install -y libvips && apt-get install -y default-mysql-client
=======
>>>>>>> 8b6288bba050eb46e72b9330de034339e4110099:pyramid-creator/prod.dockerfile

RUN apt-get update && apt-get install -y libvips

COPY requirements.txt /

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./app /app
