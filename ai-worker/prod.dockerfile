FROM python:3.9-slim
ENV PYTHONPATH "${PYTHONPATH}:/app/"

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY ai.requirements.txt /
RUN pip install -r ai.requirements.txt

COPY torch.requirements.txt /
RUN pip install -r torch.requirements.txt

COPY clearml.requirements.txt /

COPY ./app /app
# COPY clearml.conf /root/clearml.conf