# Build context is the repository root (see docker-compose.yml): the site lives
# in site/, and the docs content and data it pulls in live at the root.

# --- Build stage ---
FROM node:20-alpine AS build
WORKDIR /app/site

COPY site/package.json site/package-lock.json ./
RUN npm ci --no-audit --no-fund

COPY . /app/
ARG GITHUB_TOKEN
ENV GITHUB_TOKEN=$GITHUB_TOKEN
RUN echo "Token present: $([ -n "$GITHUB_TOKEN" ] && echo yes || echo no), length: ${#GITHUB_TOKEN}"
RUN npm run build

# --- Serve stage ---
FROM nginx:alpine

COPY --from=build /app/site/dist /usr/share/nginx/html
COPY site/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --quiet --tries=1 --spider http://127.0.0.1/ || exit 1
