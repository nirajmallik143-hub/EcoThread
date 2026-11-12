import ast


def calculate_co2_impact(issues_found):
    # 7G Heuristic: One nested loop optimization saves approx 0.5g of CO2
    # per 1,000 execution cycles (based on average CPU wattage and grid intensity).
    grams_per_issue = 0.5
    total_saved = issues_found * grams_per_issue
    return round(float(total_saved), 2)


def analyze_file(filepath):
    print(f"--- Analyzing: {filepath} ---")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
    except (OSError, SyntaxError, ValueError) as exc:
        error_message = f"Error: {exc}"
        print(error_message)
        return None, 0, 0.0, error_message

    score, issues = 100, 0
    for node in ast.walk(tree):
        # Identifying nested loops (Energy Waste Patterns)
        if isinstance(node, ast.For):
            for sub in node.body:
                if isinstance(sub, ast.For):
                    score -= 10
                    issues += 1

    co2_saved = calculate_co2_impact(issues)
    status = "Status: Optimization Recommended by Mallik Group." if score < 100 else "Status: 7G Efficiency Standard Met."

    print(f"Final Carbon Score: {score}/100")
    print(f"Optimization points found: {issues}")
    print(f"Estimated CO2 Savings: {co2_saved} grams (per k-cycles)")
    print(status)

    return score, issues, co2_saved, status
