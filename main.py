import sys
from ecothread import analyze_file


def main():
    if len(sys.argv) != 3 or sys.argv[1] != "analyze":
        print("Usage: python main.py analyze <file.py>")
        raise SystemExit(1)

    analyze_file(sys.argv[2])


if __name__ == "__main__":
    main()
