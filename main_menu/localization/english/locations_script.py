from pathlib import Path
import re

# Your input list
INPUT_FILE = Path("locations.txt")

# Folder containing your localisation files
LOCALISATION_DIR = Path("location_names")

# Output file
OUTPUT_FILE = Path("extracted_localisation.txt")

# Read IDs
ids = {
    line.strip()
    for line in INPUT_FILE.read_text(encoding="utf-8-sig").splitlines()
    if line.strip()
}

# Match localisation keys at the beginning of a line
pattern = re.compile(
    r"^\s*(" + "|".join(re.escape(x) for x in sorted(ids, key=len, reverse=True))
    + r")\s*:"
)

found = {}
extensions = {".yml", ".yaml", ".txt"}

# Search all localisation files, including subfolders
for file in LOCALISATION_DIR.rglob("*"):
    if not file.is_file() or file.suffix.lower() not in extensions:
        continue

    text = file.read_text(encoding="utf-8-sig", errors="replace")

    for line in text.splitlines():
        match = pattern.match(line)

        if match:
            key = match.group(1)
            found.setdefault(key, []).append(line)

# Write results in the same order as the input list
with OUTPUT_FILE.open("w", encoding="utf-8") as output:
    for key in sorted(ids):
        for line in found.get(key, []):
            output.write(line + "\n")

print(f"Requested IDs: {len(ids)}")
print(f"IDs found: {len(found)}")
print(f"IDs missing: {len(ids - found.keys())}")
print(f"Output: {OUTPUT_FILE.resolve()}")

if ids - found.keys():
    print("\nMissing IDs:")
    print(", ".join(sorted(ids - found.keys())))