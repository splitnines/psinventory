from __future__ import annotations
from typing import Any
from pathlib import Path
import json
import sys


def read_files(directory: Path) -> list[list[dict[Any, Any]]]:
    prop_list: list[list[dict[Any, Any]]] = []
    for file in directory.iterdir():
        if file.is_file:
            with open(file, "r") as f:
                data = json.load(f)
        prop_list.append(data.get("propList"))

    return prop_list


def prop_count(prop_list: list[list[dict[Any, Any]]]) -> dict[str, int]:
    prop_dict: dict[str, int] = {}
    for stage in prop_list:
        for prop_name in stage:
            if prop_name["propName"] in prop_dict:
                prop_dict[prop_name["propName"]] += 1
            else:
                prop_dict[prop_name["propName"]] = 1

    return dict(sorted(prop_dict.items()))


def main():

    prop_list = read_files(Path(sys.argv[1]))
    prop_dict = prop_count(prop_list)

    print(json.dumps(prop_dict, indent=2))


if __name__ == "__main__":
    main()
