"""Create one verified, non-overwriting backup of an existing project file."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
from uuid import uuid4


class BackupError(Exception):
    """A prerequisite failed; the source must not be edited."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def obvious_secret_name(path: Path) -> bool:
    name = path.name.lower()
    return (
        name == ".env"
        or name.startswith(".env.")
        or name in {"id_rsa", "id_ed25519", ".npmrc", ".pypirc", "credentials.json"}
        or name.startswith("secret.")
        or path.suffix.lower() in {".pem", ".p12", ".pfx", ".key"}
    )


def backup_file(project_root: Path, source: Path, backup_root: Path) -> dict[str, object]:
    root = project_root.resolve(strict=True)
    target = source.resolve(strict=True)
    store = backup_root.resolve(strict=True)

    if not root.is_dir() or not store.is_dir():
        raise BackupError("Project root and backup root must be existing directories.")
    if source.is_symlink() or not target.is_file():
        raise BackupError("Source must be a regular file, not a symlink.")
    if target != root and root not in target.parents:
        raise BackupError("Source is outside the project root.")
    if store == root or root in store.parents:
        raise BackupError("Backup root must be outside the project.")
    if obvious_secret_name(source):
        raise BackupError("Likely secret: use a protected backup procedure instead.")

    relative = target.relative_to(root)
    before_size = target.stat().st_size
    before_hash = sha256_file(target)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = store / f"{stamp}_{uuid4().hex[:12]}"
    run_dir.mkdir(mode=0o700)
    destination = run_dir / relative
    destination.parent.mkdir(parents=True, exist_ok=True)

    # Exclusive create prevents a collision from replacing an earlier backup.
    with target.open("rb") as original, destination.open("xb") as copy:
        shutil.copyfileobj(original, copy, length=1024 * 1024)
        copy.flush()
        os.fsync(copy.fileno())

    after_size = target.stat().st_size
    after_hash = sha256_file(target)
    copy_size = destination.stat().st_size
    copy_hash = sha256_file(destination)
    if (before_size, before_hash) != (after_size, after_hash):
        raise BackupError(f"Source changed during backup; inspect {run_dir}.")
    if (before_size, before_hash) != (copy_size, copy_hash):
        raise BackupError(f"Backup verification failed; inspect {run_dir}.")

    receipt: dict[str, object] = {
        "status": "verified",
        "source": str(target),
        "backup": str(destination),
        "bytes": before_size,
        "sha256": before_hash,
        "created_utc": stamp,
    }
    manifest = run_dir / "receipt.json"
    with manifest.open("x", encoding="utf-8") as stream:
        json.dump(receipt, stream, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    receipt["receipt"] = str(manifest)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--backup-root", required=True, type=Path)
    args = parser.parse_args()
    try:
        receipt = backup_file(args.project_root, args.source, args.backup_root)
    except (BackupError, OSError, ValueError) as error:
        print(f"BACKUP FAILED: {error}", file=sys.stderr)
        return 1
    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
