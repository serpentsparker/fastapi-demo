# fastapi-demo

A simple RESTful API in Python using the FastAPI framework.

## Description

This project demonstrates a clean implementation of a RESTful API in Python using the [FastAPI framework](https://fastapi.tiangolo.com/). Its purpose is to provide HTTP endpoints related to creating, reading, updating, and deleting actors from a PostgreSQL database. The [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/index.html) is used to map rows from the `actor` table in the database to the `Actor` domain model of this application.

## Getting Started

The application is designed to run as a Docker container on Docker Compose, Docker Swarm or Kubernetes. For local use and development refer to the [Local Development](#local-development) section.

### Dependencies

* [Docker](https://docs.docker.com/get-docker/)

To use the Kubernetes manifests of this project, a Kubernetes cluster is required. [minikube](https://minikube.sigs.k8s.io/docs/) allows to quickly setup a local Kubernetes cluster.

### Installation with Docker Compose

Clone this project and start the application stack with Docker Compose using `docker compose up -d`.

Please note that the application requires environment variables to be set in your environment. Refer to the [configuration](#configuration) section for a list of environment variables.

Alternatively, run the standalone API server with `docker run -p 8080:8080 ghcr.io/serpentsparker/fastapi-demo`. Please note that this setup requires an external PostgreSQL database.

### Installation on Kubernetes

Clone this project and deploy the application stack to a Kubernetes cluster with `kubectl apply -f ./manifests`.

Please note that the Kubernetes manifests do not provide an Ingress. To access the API on a local minikube Kubernetes cluster, run `minikube tunnel` to create a tunnel from your local machine to the Kubernetes service.

## Configuration

Set environment variables to configure the application.

| Variable Name | Description | Default | Required |
|------|-------------|------|:--------:|
| DATABASE_HOST | The hostname of the PostgreSQL database server. | "127.0.0.1" | no |
| DATABASE_PORT | The port of the PostgreSQL database server. | "5432" | no |
| DATABASE_NAME | The hostname of the PostgreSQL database server. | "myapi" | no |
| DATABASE_USER | The hostname of the PostgreSQL database server. | - | yes |
| DATABASE_PASSWORD | The hostname of the PostgreSQL database server. | - | yes |

## Local Development

This project uses [Python](https://www.python.org/) 3.12 or later. The [uv](https://docs.astral.sh/uv/) package manager is used for project and dependency management.

Run `uv sync --all-extras --dev` to install all application dependencies in a virtual environment.

Define the required environment variables using a `.env` file. Refer to [.env.example](.env.example) for an example environment file.

Start a local database with Docker Compose using `docker compose up -d database database-migrations`.

Start a local web server with `uv run --env-file .env uvicorn myapi.main:app`.

## License

This project is licensed under the MIT License. For details refer to the [LICENSE.md](LICENSE.md) file.
