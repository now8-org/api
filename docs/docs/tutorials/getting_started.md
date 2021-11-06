# Getting started

## Installation

Run `pip install .`.

### Development

To install also the development dependencies, run
`pip install -r requirements-dev.txt`

## Configuration

The following environment variables must be defined for each city
(e.g., `MADRID_DB_NAME`) with the database (PostgreSQL) connection
settings:

```bash
CITY_DB_NAME=
CITY_DB_HOST=
CITY_DB_USER=
CITY_DB_PASS=
CITY_DB_PORT=
```

You can define them in several ways:

  * manually using `export`
  * sourcing a script with the `export` commands
  * saving them in your `virtualenv` `postactivate` script
  * ...

## Running

Before running `now8_api`, start a PostgreSQL database. This can be done
with:

```bash
docker run -d --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:alpine
```

You don't need to bind the host port if both `now8_api` and the database
are running in Docker in the same network. Nevertheless, it might be
useful to bind the host port if using the database for development
so that you can run the code and tests directly from the sources.

In this case, the database configuration environment variables for
`now8_api` should be:

```bash
CITY_DB_NAME=postgres
CITY_DB_HOST=postgres
CITY_DB_USER=postgres
CITY_DB_PASS=postgres
CITY_DB_PORT=5432
```

If you are using a Python virtual environment, you can add them to
`$VIRTUAL_ENV/bin/postactivate` adding `export ` before each one of them.

### Development

For development, you can run the project with:

```bash
uvicorn now8_api.entrypoints.api.main:api --reload
```

You can then access the API at <http://localhost:8000> and the [Swagger UI](https://swagger.io/tools/swagger-ui/) (interactive API documentation) at <http://localhost:8000/docs>.

### Production

For production, a process manager is recommended to handle multiple
workers, such as `gunicorn`.

For example:

```bash
gunicorn -b 0.0.0.0:8000 -w 4 -k uvicorn.workers.UvicornWorker now8_api.entrypoints.api.main:api
```

Options:

* `-b` option specifies the binding host and port.
* `-w` option specifies the number of workers.
* `-k` option specifies the type of workers, that need to be `uvicorn.workers.UvicornWorker` as specified at the [Uvicorn Documentation](https://www.uvicorn.org/deployment/).
