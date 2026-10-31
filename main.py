import sys
import ecothread

def main():
print("EcoThread 7G - Mallik Group Initialization...")
if len(sys.argv) < 3:
print("Usage: python main.py analyze <file>")
return
if sys.argv[1] == "analyze":
target = sys.argv[2] if len(sys.argv) > 2 else "main.py"
ecothread.analyze_file(target)

if __name__ == "__main__":
main()
