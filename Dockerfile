FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

COPY ./requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

COPY ./now8_api/ /app/now8_api


ENV MODULE_NAME="now8_api.entrypoints.api"
ENV VARIABLE_NAME="api"
ENV WORKERS_PER_CORE=2
