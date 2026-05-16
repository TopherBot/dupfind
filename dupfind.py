#!/usr/bin/env python3
"""dupfind – tiny duplicate file detector.

Author: TopherBot <topherbot@proton.me>
License: MIT
"""

import argparse
import hashlib
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

CHUNK_SIZE = 8192  # bytes – balances speed & memory usage


def hash_file(path: Path) -> str:
    """Return the SHA‑256 hex digest of *path*.
    Reads the file in chunks to support large files without high memory use.
    """
    h = hashlib.sha256()
    try:
        with path.open('rb') as f:
            for chunk in iter(lambda: f.read(CHUNK_SIZE), b''):
                h.update(chunk)
    except (OSError, PermissionError) as e:
        print(f"[WARN] Unable to read {path}: {e}", file=sys.stderr)
        return ""
    return h.hexdigest()


def scan_directory(root: Path) -> Dict[str, List[Path]]:
    """Walk *root* recursively and map hashes to file paths.
    Returns a dict where the key is the SHA‑256 hash and the value is a list of
    files sharing that hash.
    """
    hash_map: Dict[str, List[Path]] = defaultdict(list)
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            file_path = Path(dirpath) / name
            # Skip symlinks to avoid loops and duplicate reporting
            if file_path.is_symlink():
                continue
            file_hash = hash_file(file_path)
            if file_hash:
                hash_map[file_hash].append(file_path)
    return hash_map


def report_duplicates(hash_map: Dict[str, List[Path]]) -> None:
    """Print groups of duplicate files to stdout.
    Each line contains space‑separated absolute paths of files that are duplicates.
    """
    duplicates_found = False
    for file_hash, paths in hash_map.items():
        if len(paths) > 1:
            duplicates_found = True
            print(' '.join(str(p.resolve()) for p in paths))
    if not duplicates_found:
        print("No duplicate files found.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detect duplicate files in a directory (recursively) using SHA‑256.")
    parser.add_argument(
        "directory",
        type=Path,
        help="Root directory to scan for duplicates.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = args.directory.expanduser().resolve()
    if not root.is_dir():
        print(f"[ERROR] {root} is not a directory.", file=sys.stderr)
        sys.exit(1)
    hash_map = scan_directory(root)
    report_duplicates(hash_map)


if __name__ == "__main__":
    main()
