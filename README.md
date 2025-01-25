# fastapi-demo

A simple RESTful API in Python using the FastAPI framework.

## Description

This project demonstrates a clean implementation of a RESTful API in Python using the [FastAPI framework](https://fastapi.tiangolo.com/). Its purpose is to provide HTTP endpoints related to creating, reading, updating, and deleting actors from a PostgreSQL database. The [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/index.html) is used to map rows from the `actor` table in the database to the `Actor` domain model of this application.

## Getting Started

The application is designed to run as a Docker container on Docker Compose, Docker Swarm or Kubernetes. For local use and development refer to the [Local Development](#local-development) section.

### Dependencies

* [Docker](https://docs.docker.com/get-docker/)
* [minikube](https://minikube.sigs.k8s.io/docs/) (for local Kubernetes only)

### Installation with Docker Compose

Clone this project to your local machine and navigate into the root directory:

```Shell
git clone https://github.com/serpentsparker/fastapi-demo.git
cd fastapi-demo
```

The Docker Compose file requires a `.env` file at the project root. If it is your first time running this application, create a new environment file from [.env.example](.env.example):

```Shell
cp .env.example .env
```

Start the complete application stack with Docker Compose:

```Shell
docker compose up -d
```

Congratulations! You have successfully deployed the API and its database on your local machine. Take a look at the [Usage](#usage) section to find out how to access and use the application.

After you have explored and used the application, stop and remove the complete application stack with Docker Compose:

```Shell
docker compose down
```

### Installation on Kubernetes

Clone this project to your local machine and navigate into the root directory:

```Shell
git clone https://github.com/serpentsparker/fastapi-demo.git
cd fastapi-demo
```

Optional: If you are using a local Kubernetes cluster with minikube, start the minikube cluster:

```Shell
minikube start
```

Deploy the complete application stack to a Kubernetes cluster with kubectl:

```Shell
kubectl apply -f ./manifests
```

Optional: If you are using a local Kubernetes cluster with minikube, create a tunnel from your local machine to the Kubernetes service:

```Shell
minikube tunnel
```

Congratulations! You have successfully deployed the API and its database to a Kubernetes cluster. Take a look at the [Usage](#usage) section to find out how to access and use the application.

After you have explored and used the application, stop and remove the local Kubernetes cluster with minikube:

```Shell
minikube delete
```

### Standalone Installation

Run the standalone API server with an external PostgreSQL database using Docker:

```Shell
docker run -p 8080:80 -e DATABASE_HOST=<DB_HOST_NAME> -e DATABASE_USER=<DB_USER> -e DATABASE_PASSWORD=<DB_PASSWORD> ghcr.io/serpentsparker/fastapi-demo
```

Refer to the [configuration](#configuration) section for a list of all environment variables.

## Usage

After a successful installation, explore the REST API documentation at `<api_url>/docs`, for example [http://localhost:8080/docs](http://localhost:8080/docs).

Once opened, you are presented with the [Swagger UI](https://swagger.io/tools/swagger-ui/) that let's you interact with the API in your browser.

The API provides an `actors` HTTP endpoint that responds to HTTP `POST`, `GET`, `PATCH`, and `DELETE` requests.

* The `HTTP POST /actors` request is used to create new actors on the database. It takes a first name and a last name, and responds with attributes that describe the created actor.
* The `HTTP GET /actors` request is used to read an existing actor from the database using its unique ID.
* The `HTTP PATCH /actors` request is used to update an existing actor on the database. It takes a new first name, a new last name, or both, and responds with attributes that describe the updated actor.
* The `HTTP DELETE /actors` request is used to delete an existing actor from the database using its unique ID.

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

This project uses [Python](https://www.python.org/) 3.12 or later. Additionally, the [uv](https://docs.astral.sh/uv/) package manager is used for project and dependency management.

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
