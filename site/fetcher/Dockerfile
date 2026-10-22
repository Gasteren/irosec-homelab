# Fetches the wiki's live data (addon stats and the activity feed) into the
# shared live-data volume. See fetch_live_data.py and docker-compose.yml.
FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATA_DIR=/data

# uid 10001 must match the /srv/live directory in site/Dockerfile, so the
# shared volume is writable here no matter which container creates it.
RUN addgroup -S -g 10001 fetcher \
 && adduser -S -D -H -u 10001 -G fetcher fetcher \
 && mkdir -p /data \
 && chown fetcher:fetcher /data

COPY fetch_live_data.py /app/fetch_live_data.py

USER fetcher

HEALTHCHECK --interval=60s --timeout=10s --start-period=60s --retries=2 \
  CMD ["python3", "/app/fetch_live_data.py", "--healthcheck"]

CMD ["python3", "/app/fetch_live_data.py"]
