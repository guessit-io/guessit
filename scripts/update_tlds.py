#!/usr/bin/env python
"""Refresh the bundled IANA top-level-domain list.

The ``website`` property matches hosts against ``guessit/data/tlds-alpha-by-domain.txt``,
the authoritative list published by IANA. New gTLDs are added over time, so a stale file
makes guessit miss modern release-site hosts (``www.<host>.party`` and friends), which then
leak into the ``title``.

Run manually (like ``scripts/gen_schema.py``); needs the network:

    uv run python scripts/update_tlds.py
"""

from __future__ import annotations

import urllib.request
from pathlib import Path

TLDS_URL = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"
TARGET = Path(__file__).resolve().parent.parent / "guessit" / "data" / "tlds-alpha-by-domain.txt"


def main() -> None:
    """Download the current IANA TLD list and overwrite the bundled copy."""
    req = urllib.request.Request(TLDS_URL, headers={"User-Agent": "guessit-tld-updater"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        content = resp.read().decode("utf-8")

    lines = content.splitlines()
    header = lines[0] if lines else ""
    count = sum(1 for line in lines[1:] if line and not line.startswith("#"))

    TARGET.write_text(content if content.endswith("\n") else content + "\n", encoding="utf-8")
    print(f"Updated {TARGET.relative_to(TARGET.parents[2])}: {count} TLDs ({header.lstrip('# ')})")


if __name__ == "__main__":
    main()
