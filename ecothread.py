import ast


def calculate_co2_impact(issues_found):
    # 7G Heuristic: One nested loop optimization saves approx 0.5g of CO2
    # per 1,000 execution cycles (based on average CPU wattage and grid intensity).
    grams_per_issue = 0.5
    total_saved = issues_found * grams_per_issue
    return total_saved


def analyze_file(filepath):
    print(f"--- Analyzing: {filepath} ---")
    try:
        with open(filepath, "r") as f:
            tree = ast.parse(f.read())

        score, issues = 100, 0
        for node in ast.walk(tree):
            # Identifying nested loops (Energy Waste Patterns)
            if isinstance(node, ast.For):
                for sub in node.body:
                    if isinstance(sub, ast.For):
                        score -= 10
                        issues += 1

        co2_saved = calculate_co2_impact(issues)

        print(f"Final Carbon Score: {score}/100")
        print(f"Optimization points found: {issues}")
        print(f"Estimated CO2 Savings: {co2_saved} grams (per k-cycles)")

        if score < 100:
            print("Status: Optimization Recommended by Mallik Group.")
        else:
            print("Status: 7G Efficiency Standard Met.")

    except Exception as e:
        print(f"Error: {e}")
