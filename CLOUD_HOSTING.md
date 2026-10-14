# Cloud hosting with a live headed browser

This deployment runs one shared Practice Studio on a Linux Docker host. The editor
includes a noVNC panel showing Chromium on an Xvfb virtual desktop. Caddy supplies
HTTPS and password authentication for the editor, API, execution WebSocket, and
desktop. Only ports 80 and 443 are published.

## Intended use

Use this deployment for yourself or people you trust with the server-side
application. All signed-in users share the desktop, browser input, snippets, and
history. Only one execution is admitted at a time. Submitted code runs with the
application user's permissions inside the container; it can access application
data and the container network. This is not a sandbox for public code submission.
Do not add cloud credentials or other secrets to the studio container.

For independent or untrusted users, provision a separate restricted execution
environment and desktop per session, with user ownership, network policy,
quotas, and artifact storage, before exposing a public service.

## Deploy on a Linux VM

1. Prepare a Linux VM with Docker Engine and Docker Compose v2. Start with 2 vCPUs
   and 4 GB RAM for one session, then measure usage. The studio container is capped
   at 2 CPUs, 3 GB RAM, and 512 processes, with 1 GB shared memory for Chromium.
2. Point a DNS A record, such as `studio.example.com`, to the VM. If you publish
   an AAAA record, it must also reach the VM. Allow inbound TCP 80 and 443; keep
   administrative SSH access restricted. Do not open 8000, 5900, or 6080.
3. Copy this project to the VM and run these commands from its root:

   ```sh
   cp .env.example .env
   docker run --rm -it caddy:2-alpine caddy hash-password
   ```

   Enter your chosen password at the prompt. Edit `.env` to set your real domain,
   username, and generated password hash. Keep single quotes around the hash so
   Compose does not interpolate its dollar signs. `.env` is excluded from Git and
   the image build. The proxy receives the hash; the studio container does not.

4. Build and launch:

   ```sh
   docker compose config --quiet
   docker compose up -d --build
   docker compose ps
   docker compose logs --tail=100 studio proxy
   ```

   The initial build downloads Python/Node dependencies and Chromium binaries.
   Caddy obtains a TLS certificate once DNS and ports are reachable. Open
   `https://studio.example.com` and enter your username and password.

5. Select **Live Browser Demo**, leave **Headed Browser** enabled, and click Run.
   Repeat with Python, JavaScript, and TypeScript. The browser opens the built-in
   login playground for 15 seconds, then closes. The desktop panel also has a
   link for a larger view in a new tab.

## Writing scripts

The headed toggle sets `HEADED=1`; ordinary scripts must honor it:

```python
browser = await p.chromium.launch(headless=os.environ.get("HEADED") != "1")
```

```javascript
const browser = await chromium.launch({ headless: process.env.HEADED !== '1' });
```

Playwright Test submissions use `--headed` automatically. Hard-coded
`headless=True`/`true` in an ordinary script overrides the user's toggle.

The desktop shows the browser only while it exists. To inspect it before closing,
add a finite wait such as `await page.wait_for_timeout(15000)` in Python or
`await page.waitForTimeout(15000)` in JavaScript. After completion, stop,
disconnect, or timeout, the runner cleans up its browser processes. Desktop
connections alone do not keep a completed run alive.

The default execution deadline is 120 seconds; change `STUDIO_TIMEOUT_SECONDS`
in `.env` and recreate the services to adjust it. Output is capped at roughly
1 MB per run. Additional executions receive a busy response rather than queueing.

Each script uses its own temporary working directory, deleted after execution.
Use `http://127.0.0.1:8000/playground/...` from submitted scripts for built-in
targets. This address refers to the application inside the cloud container.
Websites running on your laptop's localhost are not reachable from the cloud.

## Persistence and operations

SQLite history and snippets live at `/data/history.db` on the `studio_data`
Docker volume. Caddy certificates also use persistent volumes. Redeploying with
`docker compose up -d --build` preserves them. Do not use `docker compose down -v`
unless you intend to delete the stored data and certificates.

To take a consistent database backup while keeping the service available:

```sh
docker compose exec studio python -c "import sqlite3; s=sqlite3.connect('/data/history.db'); d=sqlite3.connect('/data/history.backup.db'); s.backup(d); d.close(); s.close()"
docker compose cp studio:/data/history.backup.db ./history.backup.db
```

Keep the API at one Uvicorn worker and one studio replica: execution and stop
tracking are process-local. The Docker health check checks the API; use the
browser smoke check below to verify the entire desktop chain.

## Deployment verification

- An unauthenticated request to `/`, `/api/history`, and `/desktop/vnc.html`
  must return HTTP 401.
- After login, `/api/status` should report Python, Node/TSX, Chromium, and
  `remote_desktop` ready.
- Run the demo in all three languages and confirm the page is visible and
  interactive in the desktop panel.
- Stop a long script and verify its browser disappears. Run a silent sleep past
  the configured deadline and verify a timeout. Close the editor during a run
  and verify that run releases its slot.
- Try a second run from another tab while the first is active; it should say busy.
- Save a snippet, restart the studio container, and confirm it persists.

If the desktop is blank, inspect `docker compose logs --tail=200 studio` for
Xvfb, x11vnc, or websockify failures. If HTTPS fails, verify DNS and port access.
If an external proxy is added, it must forward WebSocket upgrades for `/ws/run`
and `/desktop/websockify` and allow connections longer than a run's deadline.

## Local development

Existing local startup commands still work. The embedded desktop is only enabled
when `STUDIO_REMOTE_DESKTOP=1`; local headed browsers continue to use your desktop.
Application regression checks: `python -m unittest discover -s tests -v`.

The cloud image and Compose stack require verification on a Docker-capable Linux
host; Docker is not available in the Windows development environment where these
deployment files were prepared.
