mport sys
from ecothread import analyze_file
from engine.refactor_ai import RefactorEngine

def main():
print("🌿 EcoThread 7G - Mallik Group Initialization...")

if len(sys.argv) < 3:
print("Usage: python main.py [analyze|refactor] [filename]")
return

command = sys.argv[1]
filename = sys.argv[2]

if command == "analyze":
analyze_file(filename)

elif command == "refactor":
with open(filename, "r") as f:
content = f.read()

print(f"📡 Interfacing with 7G AI Engine for {filename}...")
engine = RefactorEngine(api_key="YOUR_KEY_HERE") # Users will input their key
result = engine.suggest_green_refactor(content)

print("\n--- Optimized Green Code ---")
print(result)
print("\n✅ Optimization Complete. Designed for Humanity.")

if __name__ == "__main__":
main()
