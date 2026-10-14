FROM node:22-bookworm-slim AS node

FROM python:3.12-slim-bookworm
COPY --from=node /usr/local/bin/node /usr/local/bin/node
COPY --from=node /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -s /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm \
    && ln -s /usr/local/lib/node_modules/npm/bin/npx-cli.js /usr/local/bin/npx

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 \
    PLAYWRIGHT_BROWSERS_PATH=/opt/playwright-browsers \
    DISPLAY=:99 PLAYWRIGHT_STUDIO_DB=/data/history.db \
    STUDIO_REMOTE_DESKTOP=1 STUDIO_MAX_RUNS=1 STUDIO_TIMEOUT_SECONDS=120

RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb x11vnc novnc websockify openbox supervisor x11-utils ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/studio
COPY requirements.txt package.json package-lock.json ./
RUN pip install --no-cache-dir -r requirements.txt \
    && npm ci --include=dev \
    && python -m playwright install --with-deps chromium \
    && node node_modules/playwright/cli.js install --with-deps chromium \
    && node node_modules/@playwright/test/cli.js install --with-deps chromium \
    && chmod -R a+rX /opt/playwright-browsers \
    && rm -rf /var/lib/apt/lists/* /root/.npm

RUN useradd --create-home --uid 10001 studio \
    && mkdir -p /data /tmp/studio-supervisor \
    && chown studio:studio /data /tmp/studio-supervisor
COPY app ./app
COPY deploy/supervisord.conf /etc/supervisor/studio.conf
COPY deploy/wait-display.sh /usr/local/bin/wait-display
RUN chmod +x /usr/local/bin/wait-display
USER studio
EXPOSE 8000 6080
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=3)"
CMD ["supervisord", "-c", "/etc/supervisor/studio.conf"]
