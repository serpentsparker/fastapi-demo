# fastapi-demo

A simple RESTful API in Python using the FastAPI framework.

## Description

This project demonstrates a clean implementation of a RESTful API in Python using the [FastAPI framework](https://fastapi.tiangolo.com/). Its purpose is to provide HTTP endpoints related to creating, reading, updating, and deleting actors from a PostgreSQL database. The [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/index.html) is used to map rows from the `actor` table in the database to the `Actor` domain model of this application.

## Getting Started

The application is designed to run as a Docker container on Docker Compose, Docker Swarm or Kubernetes. For local use and development refer to the [Local Development](#local-development) section.

### Dependencies

* [Docker](https://docs.docker.com/get-docker/)
* [minikube](https://minikube.sigs.k8s.io/docs/) (for local Kubernetes only)

### Standalone Installation

Run the standalone API server with an external PostgreSQL database using

```Shell
docker run -p 8080:8080 -e DATABASE_HOST=<DB_HOST_NAME> -e DATABASE_USER=<DB_USER> -e DATABASE_PASSWORD=<DB_PASSWORD> ghcr.io/serpentsparker/fastapi-demo
```

Refer to the [configuration](#configuration) section for a list of all environment variables.

### Installation with Docker Compose

Clone this project and start the complete application stack with Docker Compose:

```Shell
cp .env.example .env
docker compose up -d
```

Please note that the Docker Compose file requires a `.env` file at the project root. Take a look at [.env.example](.env.example) for an example environment file.

### Installation on Kubernetes

Clone this project and deploy the complete application stack to a Kubernetes cluster with kubectl:

```Shell
kubectl apply -f ./manifests
```

Please note that the Kubernetes manifests do not specify an Ingress. To access the API on a local minikube Kubernetes cluster, create a tunnel from your local machine to the Kubernetes service:

```Shell
minikube tunnel
```

## Configuration

Refer to the table below for a list of environment variables that can be used to configure the application.

| Variable Name | Description | Default | Required |
|------|-------------|------|:--------:|
| DATABASE_HOST | The hostname of the PostgreSQL database server. | - | yes |
| DATABASE_PORT | The port of the PostgreSQL database server. | "5432" | no |
| DATABASE_NAME | The hostname of the PostgreSQL database server. | "myapi" | no |
| DATABASE_USER | The hostname of the PostgreSQL database server. | - | yes |
| DATABASE_PASSWORD | The hostname of the PostgreSQL database server. | - | yes |

## Local Development

This project uses [Python](https://www.python.org/) 3.12 or later. The [uv](https://docs.astral.sh/uv/) package manager is used for project and dependency management.

### Development Dependencies

* [Python >=3.12](https://www.python.org/)
* [uv >=0.5.0](https://docs.astral.sh/uv/)
* [pre-commit >=4.0.0](https://pre-commit.com/)

### Typical Development Workflow

Run `uv sync --all-extras --dev` to install all application dependencies in a virtual environment.

Create the required `.env` file from [.env.example](.env.example) with `cp .env.example .env`.

Start a local database with Docker Compose using `docker compose up -d database database-migrations`.

Start a local web server with `uv run --env-file .env uvicorn myapi.main:app`.

### Contributing

Install Git pre-commit hooks with `pre-commit install`.

Test the Python application using pytest with `uv run python -m pytest tests`.

## License

This project is licensed under the MIT License. For details refer to the [LICENSE](LICENSE) file.
