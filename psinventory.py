from __future__ import annotations
from typing import Any
from pathlib import Path
from datetime import datetime as dt
import json
import argparse


def cli_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="psinventory.py",
        description="Creates an inventory list from Practisim stage files.",
    )

    p.add_argument("path", help="The path to the stage files.")

    p.add_argument(
        "-c",
        "--csv",
        action="store_true",
        help="Save inventory list to a CSV file  i the current directory.",
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
    ts = dt.now().strftime("%Y%m%d_%H%M%S")
    filename = f"practisim-inventory_{ts}.md"
    with open(filename, "w") as f:
        f.write("\n| Item | Count |\n")
        f.write("|---|---|\n")
        for item, count in data.items():
            f.write(f"| {item} | {count} |\n")

    print(f"\n\tMarkdown table saved to: {filename}")


def csv_out(data: dict[str, int]) -> None:
    ts = dt.now().strftime("%Y%m%d_%H%M%S")
    filename = f"practisim-inventory_{ts}.csv"
    with open(filename, "w") as f:
        f.write("Item,Count\n")
        for item, count in data.items():
            f.write(f"{item},{count}\n")

    print(f"\n\tCSV data saved to: {filename}")


def read_files(directory: Path) -> list[list[dict[Any, Any]]]:
    prop_dict: list[list[dict[Any, Any]]] = []
    for file in directory.iterdir():
        if file.is_file:
            with open(file, "r") as f:
                data = json.load(f)
        prop_dict.append(data.get("propList"))

    return prop_dict


def prop_count(prop_list: list[list[dict[Any, Any]]]) -> dict[str, int]:
    prop_dict: dict[str, int] = {}
    for stage in prop_list:
        for prop_name in stage:
            if prop_name["propName"] in prop_dict:
                prop_dict[prop_name["propName"]] += 1
            else:
                prop_dict[prop_name["propName"]] = 1

    return dict(sorted(prop_dict.items()))


def main() -> None:
    args = cli_args()

    path = Path(args.path)
    prop_list = read_files(path)
    inventory = prop_count(prop_list)

    if args.quiet is False:
        print(json.dumps(inventory, indent=2))

    if args.csv is True:
        csv_out(inventory)

    if args.markdown is True:
        md_out(inventory)


if __name__ == "__main__":
    main()
