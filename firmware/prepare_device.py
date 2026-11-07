#!/usr/bin/env python3
"""Prepare a separate firmware configuration and credentials for one unit."""

import argparse
import base64
import re
import secrets
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Create a private, uniquely credentialed Optical Audio Bridge build directory."
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

    api_key = base64.b64encode(secrets.token_bytes(32)).decode("ascii")
    ota_password = secrets.token_urlsafe(24)
    (target / "optical-audio-bridge.yaml").write_text(
        template.read_text(encoding="utf-8"), encoding="utf-8"
    )
    (target / "secrets.yaml").write_text(
        "# Private credentials for one unit. Do not share publicly.\n"
        f'optical_api_encryption_key: "{api_key}"\n'
        f'optical_ota_password: "{ota_password}"\n',
        encoding="utf-8",
    )
    print(f"Prepared private device directory: {target}")
    print("Back it up securely and share its API key with the device owner privately.")


if __name__ == "__main__":
    main()
