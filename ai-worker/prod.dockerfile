FROM python:3.9-slim
ENV PYTHONPATH "${PYTHONPATH}:/app/"

RUN rm -rf /usr/share/dotnet
RUN rm -rf /opt/ghc
RUN rm -rf "/usr/local/share/boost"
RUN rm -rf "$AGENT_TOOLSDIRECTORY"

COPY ai.requirements.txt /
RUN pip install -r ai.requirements.txt

COPY torch.requirements.txt /
RUN pip install -r torch.requirements.txt

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY clearml.requirements.txt /

COPY ./app /app
