# syntax=docker/dockerfile:1
# Minimal, frequently rebuilt bases (Chainguard's free python images), pinned by digest. The -dev
# image has pip and a shell for building the venv; the runtime image has neither.
ARG BUILD=cgr.dev/chainguard/python:latest-dev@sha256:c0328ed1997b6826d7d2ae4ea972345d3487a80f15ceb1d26f211f7c02f8c177
ARG BASE=cgr.dev/chainguard/python:latest@sha256:4b2cec05cea94a58e635f21ca5d7c642d24ec58258008bf9341a0c062de5d99d

FROM ${BUILD} AS build
WORKDIR /app
COPY requirements.txt .
RUN python -m venv /app/venv && /app/venv/bin/pip install --no-cache-dir -r requirements.txt

FROM ${BASE}
WORKDIR /app
COPY --from=build /app/venv /app/venv
COPY app.py .
COPY templates/ templates/
ARG APP_COMMIT=dev
ENV PATH=/app/venv/bin:$PATH APP_COMMIT=$APP_COMMIT PYTHONDONTWRITEBYTECODE=1
USER 65532
EXPOSE 8080
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "4", "--worker-tmp-dir", "/tmp", "--access-logfile", "-", "app:app"]
