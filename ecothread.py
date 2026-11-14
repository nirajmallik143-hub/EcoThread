"""Static Python efficiency checks and explicit, input-based CO2 estimates.

Static findings are review prompts, not measurements of runtime, energy, or emissions.
"""

import ast
import math
from pathlib import Path
from typing import Optional


def calculate_co2_impact(
    issues_found=0,
    *,
    before_seconds: Optional[float] = None,
    after_seconds: Optional[float] = None,
    power_w: Optional[float] = None,
    grid_intensity_g_per_kwh: Optional[float] = None,
) -> Optional[float]:
    """Estimate grams of CO2 saved from measured runtimes and supplied inputs.

    ``issues_found`` is retained for compatibility with earlier callers but is
    deliberately not used: a static finding cannot establish energy savings.
    Power is assumed constant across both runs. Returns ``None`` unless all
    measurements/assumptions are supplied.
    """
    values = (before_seconds, after_seconds, power_w, grid_intensity_g_per_kwh)
    if any(value is None for value in values):
        return None

    before_seconds, after_seconds, power_w, grid_intensity_g_per_kwh = map(float, values)
    if not all(math.isfinite(value) for value in values):
        raise ValueError("measurement inputs must be finite numbers")
    if before_seconds < 0 or after_seconds < 0 or power_w < 0 or grid_intensity_g_per_kwh < 0:
        raise ValueError("measurement inputs cannot be negative")
    if before_seconds < after_seconds:
        raise ValueError(
            "before_seconds must be greater than or equal to after_seconds for a CO2 reduction estimate"
        )

    # Wh = W * seconds / 3600; convert Wh to kWh, then multiply by g CO2/kWh.
    energy_saved_kwh = power_w * (before_seconds - after_seconds) / 3_600_000
    return round(energy_saved_kwh * grid_intensity_g_per_kwh, 6)


def analyze_source(source: str):
    """Return a bounded heuristic score and review findings for Python source."""
    tree = ast.parse(source)
    findings = []

    for node in ast.walk(tree):
        if not isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
            continue
        has_nested_loop = any(
            isinstance(child, (ast.For, ast.AsyncFor, ast.While))
            for child in ast.walk(node)
            if child is not node
        )
        if has_nested_loop:
            findings.append(
                f"Line {node.lineno}: loop contains another loop; review whether repeated work can be reduced."
            )

    score = max(0, 100 - 10 * len(findings))
    return score, findings


def analyze_file(
    filepath,
    *,
    before_seconds=None,
    after_seconds=None,
    power_w=None,
    grid_intensity_g_per_kwh=None,
):
    """Analyze a Python file, print findings, and return a result tuple."""
    path = Path(filepath)
    print(f"--- Analyzing: {filepath} ---")
    try:
        source = path.read_text(encoding="utf-8")
        score, findings = analyze_source(source)
    except (OSError, SyntaxError, ValueError) as exc:
        error_message = f"Error: {exc}"
        print(error_message)
        return None, 0, None, error_message

    co2_saved = calculate_co2_impact(
        len(findings),
        before_seconds=before_seconds,
        after_seconds=after_seconds,
        power_w=power_w,
        grid_intensity_g_per_kwh=grid_intensity_g_per_kwh,
    )
    print(f"Efficiency review score (heuristic): {score}/100")
    print(f"Review findings: {len(findings)}")
    for finding in findings:
        print(f"- {finding}")
    if co2_saved is None:
        print("CO2 savings: Not measured (provide before/after runtime, power, and grid intensity)")
    else:
        print(f"Estimated CO2 savings: {co2_saved} g (based on supplied measurements/assumptions)")

    status = "Review the findings; nested loops are not automatically inefficient." if findings else "No nested-loop patterns flagged by this heuristic."
    return score, len(findings), co2_saved, status

