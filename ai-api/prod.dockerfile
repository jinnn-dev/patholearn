FROM python:3.11-slim
ENV PYTHONPATH "${PYTHONPATH}:/app/"

RUN apt-get update && apt-get install -y supervisor -y build-essential
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY requirements.txt /

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN rm -rf /usr/share/dotnet
RUN rm -rf /opt/ghc
RUN rm -rf "/usr/local/share/boost"
RUN rm -rf "$AGENT_TOOLSDIRECTORY"

COPY ./app /app
COPY entry.sh /
ENTRYPOINT [ "/entry.sh" ]
