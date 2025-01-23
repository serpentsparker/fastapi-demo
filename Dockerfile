FROM python:3.13-slim AS builder

# Install the uv package manager.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Disable installer metadata, to create a deterministic layer.
ENV UV_NO_INSTALLER_METADATA=1

# Enable copy mode to support bind mount caching.
ENV UV_LINK_MODE=copy

# Omit any local packages (`--no-emit-workspace`) and development dependencies (`--no-dev`).
# This ensures that the Docker layer cache is only invalidated when the `pyproject.toml` or `uv.lock`
# files change, but remains robust to changes in the application code.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv export --frozen --no-emit-workspace --no-dev --no-editable -o requirements.txt && \
    uv pip install -r requirements.txt --target /usr/src/app


FROM python:3.13-slim

WORKDIR /myapi

# Copy the runtime dependencies from the builder stage.
COPY --from=builder /usr/src/app /myapi

# Copy the application code.
COPY . /myapi

ENV UVICORN_HOST=0.0.0.0
ENV UVICORN_PORT=80

EXPOSE 80

# Set the AWS Lambda handler.
ENTRYPOINT [ "python3", "-m", "uvicorn", "myapi.main:app" ]
