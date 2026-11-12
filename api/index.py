import os
import sys
import ast
from flask import Flask, render_template_string, request

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from ecothread import calculate_co2_impact

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>EcoThread Carbon Analyzer</title>
    <style>
      :root {
        --bg: #0b1220;
        --panel: #121b2d;
        --panel-alt: #1a2944;
        --primary: #7ae582;
        --text: #e8f1ff;
        --muted: #aabbd1;
        --danger: #ff7b72;
      }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        font-family: Arial, sans-serif;
        background: linear-gradient(135deg, #07111d 0%, #0d1c2d 100%);
        color: var(--text);
      }
      .container {
        max-width: 1080px;
        margin: 40px auto;
        padding: 24px;
      }
      .hero {
        background: rgba(18, 27, 45, 0.9);
        border: 1px solid rgba(122, 229, 130, 0.3);
        border-radius: 18px;
        padding: 30px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.25);
      }
      h1 {
        margin-top: 0;
        font-size: clamp(2rem, 5vw, 3rem);
        color: var(--primary);
      }
      .grid {
        display: grid;
        grid-template-columns: 1.2fr 0.8fr;
        gap: 24px;
        margin-top: 24px;
      }
      textarea {
        width: 100%;
        min-height: 420px;
        background: #08121d;
        color: var(--text);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 18px;
        font-size: 14px;
        line-height: 1.6;
        resize: vertical;
      }
      .panel {
        background: rgba(18, 27, 45, 0.9);
        border-radius: 14px;
        padding: 20px;
        border: 1px solid rgba(255,255,255,0.08);
      }
      .stats {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 16px;
        margin-top: 18px;
      }
      .stat {
        background: var(--panel-alt);
        border-radius: 12px;
        padding: 16px;
      }
      .label {
        color: var(--muted);
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
      }
      .value {
        font-size: 2rem;
        margin-top: 12px;
        font-weight: 700;
      }
      button {
        width: 100%;
        margin-top: 18px;
        border: none;
        border-radius: 12px;
        background: linear-gradient(120deg, #7ae582, #34d399);
        color: #06130c;
        font-weight: 800;
        padding: 14px 16px;
        font-size: 1rem;
        cursor: pointer;
      }
      .status {
        margin-top: 18px;
        padding: 14px 16px;
        border-radius: 12px;
        background: rgba(122, 229, 130, 0.1);
        color: #d9fbe2;
        border: 1px solid rgba(122, 229, 130, 0.25);
      }
      .status.bad {
        background: rgba(255, 123, 114, 0.12);
        border: 1px solid rgba(255, 123, 114, 0.32);
        color: #ffd8d3;
      }
      .footer {
        margin-top: 20px;
        color: var(--muted);
        font-size: 0.9rem;
      }
      @media (max-width: 820px) {
        .grid {
          grid-template-columns: 1fr;
        }
      }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="hero">
        <h1>EcoThread</h1>
        <p>The 7G-inspired carbon-aware code optimizer for Python efficiency analysis.</p>
        <form method="post">
          <div class="grid">
            <div>
              <textarea name="code" placeholder="Paste Python code here...">def main():
    items = [1, 2, 3]
    for x in items:
        for y in items:
            print(x, y)

main()</textarea>
            </div>
            <div class="panel">
              <div class="label">Carbon score</div>
              <div class="value">{{ score }}/100</div>
              <div class="stats">
                <div class="stat">
                  <div class="label">Issues</div>
                  <div class="value" style="font-size: 1.6rem;">{{ issues }}</div>
                </div>
                <div class="stat">
                  <div class="label">CO₂ saved</div>
                  <div class="value" style="font-size: 1.5rem;">{{ co2 }}g</div>
                </div>
              </div>
              <div class="status {{ 'bad' if score < 100 else '' }}">
                {{ status }}
              </div>
              <button type="submit">Analyze code</button>
            </div>
          </div>
        </form>
        <div class="footer">EcoThread helps detect nested-loop inefficiencies and estimate carbon impact per k-cycles.</div>
      </div>
    </div>
  </body>
</html>
"""


def analyze_python_code(code: str):
    tree = ast.parse(code)
    score = 100
    issues = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.For):
            for sub in node.body:
                if isinstance(sub, ast.For):
                    score -= 10
                    issues += 1

    co2_saved = calculate_co2_impact(issues)
    status = "Status: Optimization Recommended by Mallik Group." if score < 100 else "Status: 7G Efficiency Standard Met."
    return score, issues, round(co2_saved, 2), status


@app.get("/")
def index():
    return render_template_string(
        HTML,
        score=100,
        issues=0,
        co2=0,
        status="Status: 7G Efficiency Standard Met.",
    )


@app.post("/")
def submit():
    code = request.form.get("code", "")

    try:
        score, issues, co2, status = analyze_python_code(code)
    except Exception as exc:
        return render_template_string(
            HTML,
            score=0,
            issues=0,
            co2=0,
            status=f"Error: {exc}",
        )

    return render_template_string(
        HTML,
        score=score,
        issues=issues,
        co2=co2,
        status=status,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
