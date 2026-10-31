import ast
import os

class EcoAnalyzer(ast.NodeVisitor):
def __init__(self):
self.carbon_score = 100
self.suggestions = []

def visit_For(self, node):
# Rule: Detect inefficient nested loops
for item in node.body:
if isinstance(item, ast.For):
self.carbon_score -= 10
self.suggestions.append(f"Line {node.lineno}: Nested loop detected. Consider vectorization or a Hash Map to reduce O(n^2) energy waste.")
self.generic_visit(node)

def visit_ListComp(self, node):
# Rule: Large list comprehensions can be memory intensive
self.suggestions.append(f"Line {node.lineno}: Consider if a Generator Expression would save memory/power.")
self.generic_visit(node)

def analyze_file(filepath):
with open(filepath, "r") as source:
tree = ast.parse(source.read())

analyzer = EcoAnalyzer()
analyzer.visit(tree)

print(f"--- EcoThread Analysis for {filepath} ---")
print(f"Final Carbon Score: {analyzer.carbon_score}/100")
print("\nOptimization Path:")
for suggestion in analyzer.suggestions:
print(f"🌱 {suggestion}")

if __name__ == "__main__":
# Test on itself for demonstration
analyze_file(__file__)
