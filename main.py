"""The Battery's Last Text to Its Charger.

Writes one line of plain text -- the phone battery's last text message
to the charger it waited for all day -- to /output/entry.txt.

Standard library only. No trailing newline in the output file.
"""

import os

ENTRY_TEXT = "You promised you'd plug me in after lunch. It's midnight now, and the toaster got charged twice."


def resolve_output_path():
    """Resolve where entry.txt goes, from the script's own directory.

    Never relies on the current working directory.
    """
    env_path = os.environ.get("ENTRY_OUTPUT")
    if env_path:
        return env_path
    for var in ("OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        base = os.environ.get(var)
        if base:
            return os.path.join(base, "entry.txt")
    return "/output/entry.txt"


def validate_entry(text):
    """Guard: the entry must be 1-200 chars, one line, valid UTF-8.

    Raises on an invalid entry; never changes the output bytes.
    """
    text.encode("utf-8")
    if not 1 <= len(text) <= 200:
        raise ValueError("entry must be 1-200 characters")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")


def main():
    validate_entry(ENTRY_TEXT)
    path = resolve_output_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
    except OSError:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY_TEXT)
    os.chmod(path, 0o644)
    # Read-back check: what landed on disk must be byte-identical.
    with open(path, "rb") as f:
        if f.read().decode("utf-8") != ENTRY_TEXT:
            raise ValueError("read-back mismatch")


if __name__ == "__main__":
    main()
