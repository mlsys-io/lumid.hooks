#!/usr/bin/env python
"""Validate that a release tag matches the package version."""

import argparse
import re
import tomllib
from pathlib import Path


_TAG_RE = re.compile(r"^v(?P<version>[0-9]+\.[0-9]+\.[0-9]+(?:[A-Za-z0-9.!+_-]*)?)$")


def _tag_version(tag: str) -> str:
    match = _TAG_RE.fullmatch(tag)
    if match is None:
        raise SystemExit(f"Release tag must be formatted as v<version>: {tag}")
    return match.group("version")


def _project_version(pyproject: Path) -> str:
    with pyproject.open("rb") as handle:
        data = tomllib.load(handle)
    version = data.get("project", {}).get("version")
    if not isinstance(version, str):
        raise SystemExit(f"Missing project.version in {pyproject}")
    return version


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True, help="Release tag, for example v0.1.0.")
    parser.add_argument(
        "--pyproject",
        default=Path("pyproject.toml"),
        type=Path,
        help="Path to pyproject.toml.",
    )
    args = parser.parse_args()

    tag_version = _tag_version(args.tag)
    project_version = _project_version(args.pyproject)
    if tag_version != project_version:
        raise SystemExit(
            f"Release tag {args.tag} does not match project.version {project_version}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
