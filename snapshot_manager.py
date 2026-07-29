import hashlib
import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


def calculate_sha256(file_path: Path) -> str:
    """Calculate SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def get_next_version(snapshot_root: str = "snapshots") -> int:
    """Get the next version number for snapshot creation."""
    snapshot_root_path = Path(snapshot_root)
    if not snapshot_root_path.exists():
        return 1

    existing_versions = []
    for item in snapshot_root_path.iterdir():
        if item.is_dir() and item.name.startswith("snapshot_"):
            parts = item.name.split("_")
            if len(parts) >= 2 and parts[1].isdigit():
                existing_versions.append(int(parts[1]))

    return max(existing_versions, default=0) + 1


def create_snapshot(
    label: str = "manual",
    target_dir: str = "test_files",
    protected_dir: Optional[str] = None,
    snapshot_root: str = "snapshots",
) -> Dict[str, object]:
    """Create a new snapshot and record original SHA-256 hashes."""
    source_dir = protected_dir if protected_dir is not None else target_dir

    snapshot_root_path = Path(snapshot_root)
    snapshot_root_path.mkdir(parents=True, exist_ok=True)

    next_version = get_next_version(snapshot_root)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_label = label.strip().replace(" ", "_") or "manual"
    snapshot_name = f"snapshot_{next_version:03d}_{timestamp}_{clean_label}"
    snapshot_dir = snapshot_root_path / snapshot_name

    source_path = Path(source_dir)
    if not source_path.exists():
        source_path.mkdir(parents=True, exist_ok=True)

    copied_files = 0
    hashes = {}

    for item in source_path.rglob("*"):
        if item.is_file():
            rel = item.relative_to(source_path)
            target = snapshot_dir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)

            hashes[str(rel)] = calculate_sha256(item)
            copied_files += 1

    manifest_path = snapshot_dir / ".hashes.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(hashes, f, indent=2)

    return {
        "version": next_version,
        "name": snapshot_name,
        "files_copied": copied_files,
        "path": str(snapshot_dir),
    }


def rollback_snapshot(
    version: int,
    target_dir: str = "test_files",
    snapshot_root: str = "snapshots",
) -> Dict[str, object]:
    """Rollback to a snapshot and perform true integrity check."""
    snapshot_root_path = Path(snapshot_root)
    if not snapshot_root_path.exists():
        return {
            "success": False,
            "message": "Snapshot root directory not found.",
        }

    snapshot_match = None
    for item in snapshot_root_path.iterdir():
        if item.is_dir() and item.name.startswith("snapshot_"):
            try:
                snap_version = int(item.name.split("_")[1])
            except ValueError:
                continue
            if snap_version == version:
                snapshot_match = item
                break

    if snapshot_match is None:
        return {
            "success": False,
            "message": f"Snapshot version {version} not found.",
        }

    manifest_path = snapshot_match / ".hashes.json"
    original_hashes = {}
    if manifest_path.exists():
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                original_hashes = json.load(f)
        except Exception:
            pass

    target_path = Path(target_dir)
    target_path.mkdir(parents=True, exist_ok=True)

    for existing in target_path.iterdir():
        if existing.is_file():
            existing.unlink()
        elif existing.is_dir():
            shutil.rmtree(existing)

    verified_files = 0
    hash_logs = []
    for item in snapshot_match.rglob("*"):
        if item.is_file() and item.name != ".hashes.json":
            rel = item.relative_to(snapshot_match)
            target_child = target_path / rel
            target_child.parent.mkdir(parents=True, exist_ok=True)

            current_snap_hash = calculate_sha256(item)

            shutil.copy2(item, target_child)

            orig_hash = original_hashes.get(str(rel), current_snap_hash)

            if current_snap_hash == orig_hash:
                verified_files += 1
                hash_logs.append(
                    f" {rel.name}: SHA-256 Verified ({current_snap_hash[:10]}...)"
                )
            else:
                hash_logs.append(
                    f" {rel.name}: Hash Mismatch! (Corrupted Backup File)"
                )

    return {
        "success": True,
        "verified_count": verified_files,
        "logs": "\n".join(hash_logs),
    }


def delete_snapshot(
    version: int, snapshot_root: str = "snapshots"
) -> Dict[str, object]:
    """Delete a specific snapshot version."""
    snapshot_root_path = Path(snapshot_root)
    if not snapshot_root_path.exists():
        return {
            "success": False,
            "message": "Snapshot root directory not found.",
        }

    for item in snapshot_root_path.iterdir():
        if item.is_dir() and item.name.startswith("snapshot_"):
            try:
                snap_version = int(item.name.split("_")[1])
            except ValueError:
                continue
            if snap_version == version:
                shutil.rmtree(item)
                return {
                    "success": True,
                    "message": f"Snapshot version {version} deleted successfully.",
                }

    return {
        "success": False,
        "message": f"Snapshot version {version} not found.",
    }


def list_snapshots(snapshot_root: str = "snapshots") -> List[Dict[str, str]]:
    """List all available snapshots sorted by version."""
    snapshot_root_path = Path(snapshot_root)
    if not snapshot_root_path.exists():
        return []

    snapshots = []
    for item in snapshot_root_path.iterdir():
        if item.is_dir() and item.name.startswith("snapshot_"):
            parts = item.name.split("_")
            if len(parts) >= 2 and parts[1].isdigit():
                version = int(parts[1])
                ctime = datetime.fromtimestamp(item.stat().st_ctime).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                snapshots.append(
                    {"version": version, "name": item.name, "created_at": ctime}
                )

    snapshots.sort(key=lambda x: x["version"])
    return snapshots