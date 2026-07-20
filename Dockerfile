FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

RUN apt-get update \
    && apt-get install --no-install-recommends -y curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY base/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r /app/requirements.txt

COPY base/ /app/
RUN mkdir -p /app/staticfiles /app/media /app/media-seed /app/logs \
    && if [ -d /app/media ]; then cp -a /app/media/. /app/media-seed/; fi \
    && chmod +x /app/entrypoint.sh

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
  CMD curl --fail --silent --show-error \
    -H "Host: ${HEALTHCHECK_HOST:-localhost}" \
    -H "X-Forwarded-Proto: https" \
    "http://127.0.0.1:${PORT:-8000}/healthz/" || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]
