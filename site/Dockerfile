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

# Git ref of this repo that the live data (/api/*.json, see the nginx config)
# is read from. The nginx image substitutes it into the config at startup.
ENV LIVE_DATA_REF=main

COPY --from=build /app/site/dist /usr/share/nginx/html
COPY site/nginx.conf.template /etc/nginx/templates/default.conf.template

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --quiet --tries=1 --spider http://127.0.0.1/ || exit 1
