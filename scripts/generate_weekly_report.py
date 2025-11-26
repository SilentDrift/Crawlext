import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))

from aggregation.weekly_report import generate


def main():
    path = generate()
    print(f"Report written to {path}")


if __name__ == "__main__":
    main()
