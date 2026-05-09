from pathlib import Path
import json
import sys

name = sys.argv[1]
src = Path(name)
dst = Path(f"{name}.recovered")

text = src.read_bytes().decode("utf-16")
text = text.replace("\x19", "'")

json.loads(text)

dst.write_text(text, encoding="utf-8", newline="\n")
print(f"Wrote {dst}")
