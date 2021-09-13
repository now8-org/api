# Docker

The HTTP API server of this project can be run using `docker`.

## Building

To build the Docker image of the HTTP API server of this project run
(from the root directory of this repository):

```bash
docker build -t local/now8-api .
```

## Running

Then, to run the server execute (filling the variable values):

```bash
docker run -d --name now8-api -p 8000:8000 -e N_WORKERS=4 local/now8-api
```

You can then access the HTTP API at <http://localhost:8000>.
