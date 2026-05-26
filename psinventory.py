from __future__ import annotations
from datetime import datetime as dt
from pathlib import Path
from typing import Any
import argparse
import csv
import json
import sys


def cli_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="psinventory.py",
        description="Creates an inventory list from Practisim stage files.",
    )

    p.add_argument("path", nargs="+", help="The path to the stage files.")

    p.add_argument(
        "-c",
        "--csv",
        action="store_true",
        help="Save inventory list to a CSV file in the current directory.",
    )

    p.add_argument(
        "-m",
        "--markdown",
        action="store_true",
        help="Save inventory list as table in a markdown file in the "
        "current directory.",
    )

    p.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Do not print raw JSON output.",
    )

    return p.parse_args()


def md_out(data: dict[str, int]) -> None:
    ts = dt.now().strftime("%Y-%m-%d_%H_%M_%S")
    filename = f"practisim-inventory_{ts}.md"
    with open(filename, "w") as f:
        f.write("\n| Item | Count |\n")
        f.write("|---|---|\n")
        for item, count in data.items():
            item = item.replace("|", "\\|")
            f.write(f"| {item} | {count} |\n")

    print(f"\n\tMarkdown table saved to: {filename}")


def csv_out(data: dict[str, int]) -> None:
    ts = dt.now().strftime("%Y%m%d_%H%M%S")
    filename = f"practisim-inventory_{ts}.csv"
    header = ["Item", "Count"]

    with open(filename, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(data.items())

    print(f"\n\tCSV data saved to: {filename}")


def get_prop_list(file: Path) -> list:
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e} - {file}")
        sys.exit()
    except Exception as e:
        print(f"Bad file: {e} - {file}")
        sys.exit()

    if not isinstance(data, dict):
        sys.exit()

    props = data.get("propList")
    if not isinstance(props, list):
        sys.exit()

    return props


def read_files(paths: list[str]) -> list[list[dict[Any, Any]]]:
    prop_list: list[list[dict[Any, Any]]] = []

    for path in paths:
        path = Path(path).expanduser()

        if not path.exists():
            print(f"path does not exist: {path}")
            continue

        if path.is_file() and path.suffix.lower() == ".stg":
            prop_list.append(get_prop_list(path))
        elif path.is_dir():
            for file in path.iterdir():
                if file.is_file() and file.suffix.lower() == ".stg":
                    prop_list.append(get_prop_list(file))

    return prop_list


def prop_count(prop_list: list[list[dict[Any, Any]]]) -> dict[str, int]:
    prop_dict: dict[str, int] = {}
    for stage in prop_list:
        for prop_name in stage:
            name = prop_name.get("propName")
            if not isinstance(name, str) or not name:
                continue

            prop_dict[name] = prop_dict.get(name, 0) + 1

    return dict(sorted(prop_dict.items()))


def main() -> None:
    args = cli_args()

    path = args.path

    prop_list = read_files(path)
    if not prop_list:
        print("No items found in any of the files provided")
        sys.exit()

    inventory = prop_count(prop_list)
    if not inventory:
        print("No items found in the inventory")
        sys.exit()

    if args.quiet is False:
        print(json.dumps(inventory, indent=2))

    if args.csv is True:
        csv_out(inventory)

    if args.markdown is True:
        md_out(inventory)


if __name__ == "__main__":
    main()
