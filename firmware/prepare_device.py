#!/usr/bin/env python3
"""Prepare a separate firmware configuration for one unit."""

import argparse
import re
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Create a separate Optical Audio Bridge build directory."
    )
    parser.add_argument("label", help="Local unit label, using letters, digits, _ or -")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", args.label):
        parser.error("label must contain only letters, digits, underscores or hyphens")

    firmware_dir = Path(__file__).resolve().parent
    template = firmware_dir / "optical-audio-bridge.yaml"
    private_root = firmware_dir / "private-devices"
    private_root.mkdir(exist_ok=True)
    target = private_root / args.label
    try:
        target.mkdir()
    except FileExistsError:
        parser.error(f"unit directory already exists: {target}; choose another label")

    (target / "optical-audio-bridge.yaml").write_text(
        template.read_text(encoding="utf-8"), encoding="utf-8"
    )
    print(f"Prepared device directory: {target}")
    print("The API and ESPHome OTA have no authentication by default; use a trusted network.")


if __name__ == "__main__":
    main()
