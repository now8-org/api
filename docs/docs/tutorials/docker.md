# Docker

The HTTP API server of this project can be run using `docker`.

## Building

To build the Docker image of the HTTP API server of this project run
(from the root directory of this repository):

```bash
docker build -t local/ntapi .
```

## Running

Then, to run the server execute (filling the variable values):

```bash
docker run --rm --name ntapi -p 8000:8000 -it -e DB_NAME='' -e DB_HOST='' -e DB_USER='' -e DB_PASS='' -e DB_PORT='5432' local/ntapi
```

You can then access the HTTP API at <http://localhost:8000>.
