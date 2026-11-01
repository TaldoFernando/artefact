"""Validate original fixtures without printing customer records."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from emporio.store import Store


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data")
    args = parser.parse_args()
    try:
        result = Store(args.data_dir).validate_data()
    except (OSError, ValueError, KeyError, ArithmeticError) as exc:
        sys.exit(f"Data validation failed: {exc}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
