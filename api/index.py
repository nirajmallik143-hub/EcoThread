"""Minimal web interface for static review; no user code is executed."""

import ast
import os
import sys
from flask import Flask, render_template_string, request

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from ecothread import analyze_source

app = Flask(__name__)

HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>EcoThread Python Review</title>
  <style>
    body { font: 16px/1.5 system-ui, sans-serif; max-width: 960px; margin: 2rem auto; padding: 0 1rem; background: #0b1220; color: #e8f1ff; }
    main { background: #121b2d; border: 1px solid #35513c; border-radius: 16px; padding: 1.5rem; }
    textarea { box-sizing: border-box; width: 100%; min-height: 340px; padding: 1rem; color: inherit; background: #08121d; border: 1px solid #526276; border-radius: 8px; font: 14px/1.5 monospace; }
    button { margin-top: 1rem; padding: .8rem 1.2rem; border: 0; border-radius: 8px; background: #7ae582; font-weight: bold; cursor: pointer; }
    .note { color: #c4d2e3; }
    .error { color: #ffaaa3; }
    li { margin: .5rem 0; }
  </style>
</head>
<body><main>
  <h1>EcoThread</h1>
  <p>Static Python review for possible repeated work. Findings are heuristic, not proof of inefficiency.</p>
  <form method="post">
    <label for="code">Python source</label>
    <textarea id="code" name="code" spellcheck="false">{{ code }}</textarea>
    <button type="submit">Analyze source</button>
  </form>
  {% if analyzed %}
    <h2>Review results</h2>
    {% if error %}<p class="error">Could not parse source: {{ error }}</p>
    {% else %}
      <p>Heuristic review score: {{ score }}/100 · Findings: {{ findings|length }}</p>
      {% if findings %}<ul>{% for finding in findings %}<li>{{ finding }}</li>{% endfor %}</ul>
      {% else %}<p>No nested-loop patterns flagged by this check.</p>{% endif %}
      <p><strong>CO₂ savings: Not measured.</strong> Static source analysis cannot establish runtime, energy use, or emissions.</p>
    {% endif %}
  {% endif %}
  <p class="note">This tool does not execute submitted code. Benchmark changes separately and provide documented power and grid-intensity data before estimating emissions.</p>
</main></body></html>"""


def analyze_python_code(code: str):
    """Return the heuristic score and findings for Python source."""
    return analyze_source(code)


@app.get("/")
def index():
    return render_template_string(HTML, code="", analyzed=False)


@app.post("/")
def submit():
    code = request.form.get("code", "")
    try:
        score, findings = analyze_python_code(code)
    except (SyntaxError, ValueError) as exc:
        return render_template_string(HTML, code=code, analyzed=True, error=str(exc))
    return render_template_string(
        HTML, code=code, analyzed=True, score=score, findings=findings, error=None
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
