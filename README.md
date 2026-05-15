# Practisim Inventory

A small Python utility for creating an inventory list from Practisim stage files.

The script reads Practisim `.STG` JSON files, extracts each stage’s `propList`, counts how many times each prop appears, and outputs the inventory as JSON, CSV, and/or Markdown.

## Requirements

- Python 3.14 or newer
- No external Python dependencies

## Project Files

- `psinventory.py` - main inventory script
- `stg_recover.py` - helper script for recovering UTF-16 stage files into UTF-8 JSON
- `pyproject.toml` - project metadata
- `uv.lock` - lock file for `uv`

## Usage

Run the inventory script with the path to a directory containing Practisim stage files:

```sh
  python psinventory.py ./data
```

By default, the script prints the inventory as formatted JSON.

Example Output:

```json
  {
    "barrel-plastic-stack": 21,
    "faultline-4ft": 48,
    "faultline-8ft": 76,
    "uspsa-full-target": 83,
    "uspsa-popper": 17,
    "wall-med-color": 52,
    "wall-short-color": 24
  }
```

Options:

### Save as CSV

```sh
  python psinventory.py ./data --csv
```

This creates a timestamped file in the current directory:

```text
  practisim-inventory_YYYYMMDD_HHMMSS.csv
```

Example CSV content:

```csv
  Item,Count
  barrel-plastic-stack,21
  faultline-4ft,48
  faultline-8ft,76
  uspsa-full-target,83
  wall-med-color,52
```

### Save as Markdown Table

```sh
  python psinventory.py ./data --markdown
```

This creates a timestamped file in the current directory:

```text
  practisim-inventory_YYYYMMDD_HHMMSS.md
```

Example Markdown content:

  | Item | Count |
  |---|---|
  | barrel-plastic-stack | 21 |
  | faultline-4ft | 48 |
  | faultline-8ft | 76 |
  | uspsa-full-target | 83 |
  | wall-med-color | 52 |


### Suppress JSON Output

```sh
  python psinventory.py ./data --quiet
```

This prevents the raw JSON inventory from being printed to the terminal.

### Combine Options

```sh
  python psinventory.py ./data --csv --markdown --quiet
```

Recovering Stage Files

Some Practisim stage files may need to be converted from UTF-16 to UTF-8 JSON.

Use stg_recover.py with the stage file path:

```sh
  python stg_recover.py path/to/file.stg
```

This writes a recovered file next to the original:

```text
  path/to/file.stg.recovered
```

The recovered file is decoded as UTF-16, replaces invalid \x19 characters with apostrophes, validates the result as JSON, and writes UTF-8
output.

Notes

- Input files are expected to be JSON stage files containing a propList field.
- Generated CSV and Markdown files are written to the current working directory.
- Files under data/, test/, and practisim-personalProps-LCSC.json are ignored by Git.
