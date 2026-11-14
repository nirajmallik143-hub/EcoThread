# Deployment

EcoThread has two deployment targets. Vercel serves the Flask web interface; Cloudflare Workers serves a lightweight Python JSON API. Both run the same nested-loop heuristic, and the reported CO₂ value is an estimate—not a measurement.

## Vercel (web interface)

1. Import `nirajmallik143-hub/EcoThread` into Vercel and keep the project root at the repository root.
2. Vercel detects `vercel.json` and installs the Flask dependency from `requirements.txt`.
3. Deploy, then open the deployment URL. The Python web app is served by `api/index.py`.

No environment variables are required. The CLI (`main.py`) is not part of the serverless web deployment.

## Cloudflare Workers (JSON API)

The Worker is implemented separately from Flask because Cloudflare Workers does not run the Vercel/Flask application entrypoint. It provides `GET /` and `GET /health` health checks, plus `POST /analyze`.

Requirements: a current `uv` installation and Cloudflare account authenticated with Wrangler.

```bash
uv sync
uv run pywrangler dev
```

Deploy with:

```bash
uv run pywrangler deploy
```

Example request:

```bash
curl -X POST https://<your-worker>.<your-subdomain>.workers.dev/analyze \
  -H 'content-type: application/json' \
  --data '{"code":"for x in xs:\n    for y in ys:\n        pass"}'
```

The API expects a JSON object with a string `code` field and limits source input to 64 KiB. Invalid JSON, Python syntax errors, unsupported routes, and oversized payloads return JSON error responses. Cloudflare's `wrangler.jsonc` selects the Python Worker entry point and enables the Python Workers compatibility flag.
