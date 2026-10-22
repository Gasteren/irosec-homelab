# Build context is the repository root (see docker-compose.yml): the site lives
# in site/, and the docs content and data it pulls in live at the root.

# --- Build stage ---
FROM node:20-alpine AS build
WORKDIR /app/site

COPY site/package.json site/package-lock.json ./
RUN npm ci --no-audit --no-fund

COPY . /app/
RUN npm run build

# --- Serve stage ---
FROM nginx:alpine

COPY --from=build /app/site/dist /usr/share/nginx/html
COPY site/nginx.conf /etc/nginx/conf.d/default.conf

# Mount point for the live-data volume written by the fetcher service (uid
# 10001, see site/fetcher/Dockerfile). Owning it here keeps the volume
# writable for the fetcher even when this container creates it.
RUN mkdir -p /srv/live && chown 10001:10001 /srv/live

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --quiet --tries=1 --spider http://127.0.0.1/ || exit 1
