"""Cloudflare Workers Python API for EcoThread."""

import ast
import json
from urllib.parse import urlsplit

from workers import Response, WorkerEntrypoint

MAX_CODE_BYTES = 64 * 1024


def json_response(payload: dict, status: int = 200) -> Response:
    return Response(
        json.dumps(payload),
        status=status,
        headers={"content-type": "application/json; charset=utf-8"},
    )


def analyze(code: str) -> dict:
    tree = ast.parse(code)
    issues = sum(
        1
        for node in ast.walk(tree)
        if isinstance(node, ast.For)
        for child in node.body
        if isinstance(child, ast.For)
    )
    score = max(0, 100 - 10 * issues)
    return {
        "score": score,
        "issues": issues,
        "estimated_co2_g": round(issues * 0.5, 2),
        "estimate_note": "Heuristic estimate only; not a measured emissions reduction.",
        "status": "optimization_review_recommended" if issues else "no_flagged_patterns",
    }


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        path = urlsplit(request.url).path.rstrip("/") or "/"
        method = request.method.upper()

        if method == "GET" and path in ("/", "/health"):
            return json_response({"service": "EcoThread", "status": "ok"})

        if path != "/analyze":
            return json_response({"error": "Not found"}, 404)
        if method != "POST":
            return json_response({"error": "Use POST /analyze"}, 405)

        raw_body = await request.text()
        if len(raw_body.encode("utf-8")) > MAX_CODE_BYTES:
            return json_response({"error": "Request body exceeds 64 KiB"}, 413)

        try:
            payload = json.loads(raw_body)
        except json.JSONDecodeError:
            return json_response({"error": "Request body must be valid JSON"}, 400)
        if not isinstance(payload, dict) or not isinstance(payload.get("code"), str):
            return json_response({"error": "Expected a JSON object with a string 'code' field"}, 400)

        try:
            return json_response(analyze(payload["code"]))
        except SyntaxError as exc:
            return json_response(
                {"error": "Invalid Python syntax", "line": exc.lineno, "column": exc.offset},
                400,
            )
