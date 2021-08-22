FROM python:3.9 as builder

RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"


COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt; \
    pip install .

FROM python:3.9-alpine

RUN apk add libc6-compat

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app

# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

EXPOSE 8000

CMD ["sh", "-c", "gunicorn -b 0.0.0.0:8000 -w ${N_WORKERS:-4} -k uvicorn.workers.UvicornWorker ntapi.entrypoints.api:api"]
