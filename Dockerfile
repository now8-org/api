FROM python:3.9 as builder

COPY . /app

WORKDIR /app

RUN pip install .

EXPOSE 8000

CMD ["sh", "-c", "gunicorn -b 0.0.0.0:8000 -w ${N_WORKERS:-4} -k uvicorn.workers.UvicornWorker now8_api.entrypoints.api:api"]
