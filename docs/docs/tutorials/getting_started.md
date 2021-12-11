# Getting started

## Installation

Run `pip install .`.

### Development

To install also the development dependencies, run
`make install`

## Configuration

Choose the city to serve for with the following environment variable:

```bash
CITY=madrid
```

Then, also define the following environment variables with the database
(PostgreSQL) connection settings:

```bash
DB_NAME=
DB_HOST=
DB_USER=
DB_PASS=
DB_PORT=
```

Ways of defining them:

* manually using `export`
* sourcing a script with the `export` commands
* saving them in your `virtualenv` `postactivate` script
* ...

## Running

Before running `now8_api`, start a PostgreSQL database with the PostGIS
extension installed. You can run:

```bash
docker run -d --name postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=postgres \
  -p 5432:5432 \
  postgis/postgis
```

You don't need to bind the host port if both `now8_api` and the database
are running in Docker in the same network
(add `--network now8` to both). Nevertheless, it might be
useful to bind the host port if using the database for development
so that you can run the code and tests directly from the sources.

In this case, the database configuration environment variables for
`now8_api` should be:

```bash
DB_NAME=postgres
DB_HOST=postgres
DB_USER=postgres
DB_PASS=postgres
DB_PORT=5432
```

Which are the default values.

If you are using a Python virtual environment, you can add them to
`$VIRTUAL_ENV/bin/postactivate` adding `export ` before each one of them.

### Development

For development, you can run the project with:

```bash
make run
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

## Populating the database

The database should contain the GTFS information for the city, it can be
populated using
[OpenTransitTools/gtfsdb](https://github.com/OpenTransitTools/gtfsdb).

For example, for adding the intercity buses information for Madrid, run:

```bash
docker run \
    --network now8 \
    local/gtfsdb \
        --database_url postgresql://postgres:postgres@postgres:5432/postgres \
        --is_geospatial \
        https://www.arcgis.com/sharing/rest/content/items/885399f83408473c8d815e40c5e702b7/data
```

Don't forget to run the PostgreSQL (with the PostGIS extension) Docker
in the same network (i.e., `now8`).
