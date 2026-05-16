# dupfind

**dupfind** is a minimal, zero‑dependency Python script that finds duplicate files in a given directory (recursively) by comparing SHA‑256 hashes.

## Usage
```bash
python dupfind.py /path/to/scan
```
The script prints groups of duplicate files, one group per line, with paths separated by a space.

## How it works
1. Walk the directory tree.
2. Compute a SHA‑256 hash for each file (chunks to handle large files).
3. Group files by identical hashes.
4. Print groups that contain more than one file.

## Why tiny?
- **No external libraries** – only the Python standard library.
- **Idempotent** – running it repeatedly yields the same result unless the filesystem changes.
- **Clear naming** – all functions and variables are self‑descriptive.

## License
MIT – see the source file header for details.
