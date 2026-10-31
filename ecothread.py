import ast

def analyze_file(filepath):
print(f"--- Analyzing: {filepath} ---")
try:
with open(filepath, "r") as f:
tree = ast.parse(f.read())
score, issues = 100, 0
for node in ast.walk(tree):
if isinstance(node, ast.For):
for sub in node.body:
if isinstance(sub, ast.For):
score -= 10
issues += 1
print(f"Final Carbon Score: {score}/100")
print(f"Optimization points found: {issues}")
except Exception as e:
print(f"Error: {e}")
