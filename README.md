# ML Pipeline Orchestrator API

This is a simple API for managing pipelines and pipeline runs, built with FastAPI.


## Prerequisites

* **Python 3.12+**
* **UV** (for dependency management) - brew install uv
* **Docker** (if using Docker Compose) - [Installation instructions](https://docs.docker.com/get-docker/)

## Installation

1.  Clone the repository:

    ```bash
    git clone <your_repository_url>
    cd ml-pipeline-orchestrator
    ```

2.  Install dependencies using UV:

    ```bash
    uv sync
    ```

## Running the Application

### Using Uvicorn


1. Start the Uvicorn server:

    ```bash
    uv run uvicorn src.app.main:app   
    ```

    This will start the application on `http://127.0.0.1:8000`. The `--reload` flag enables hot reloading, so the server will automatically restart when you make changes to the code.

### Using Docker Compose (Recommended)

1.  Build and run the Docker containers:

    ```bash
    docker compose build
    docker compose up
    ```

    This will build the Docker image and start the container in detached mode. The application will be accessible at `http://127.0.0.1:8000`.

## Unit Testing the API

 (Incomplete) The application includes some basic suites of tests that can be run using `pytest`. [most currently failing]

## API Documentation and Manual Testing

The API is documented using Swagger UI. Once the application is running, you can access the documentation and manually test at:

* `http://127.0.0.1:8000/docs`
* `http://127.0.0.1:8000/redoc`
