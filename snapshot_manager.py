# import os
# import shutil
# from datetime import datetime
# from pathlib import Path
# from typing import Dict, List, Optional


# def create_snapshot(target_dir: str = "test_files", snapshot_root: str = "snapshots", label: str = "") -> Dict[str, object]:
#     target_path = Path(target_dir)
#     snapshot_root_path = Path(snapshot_root)
#     snapshot_root_path.mkdir(parents=True, exist_ok=True)

#     versions = [p for p in snapshot_root_path.iterdir() if p.is_dir() and p.name.startswith("snapshot_")]
#     version_number = len(versions) + 1

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     snapshot_name = f"snapshot_{version_number:03d}_{timestamp}"
#     if label:
#         snapshot_name = f"{snapshot_name}_{label.replace(' ', '_')}"

#     snapshot_path = snapshot_root_path / snapshot_name
#     snapshot_path.mkdir(parents=True, exist_ok=True)

#     if target_path.exists():
#         for item in target_path.iterdir():
#             if item.is_file():
#                 shutil.copy2(item, snapshot_path / item.name)
#             elif item.is_dir():
#                 dest_dir = snapshot_path / item.name
#                 dest_dir.mkdir(parents=True, exist_ok=True)
#                 for child in item.rglob("*"):
#                     if child.is_file():
#                         rel = child.relative_to(item)
#                         target_child = dest_dir / rel
#                         target_child.parent.mkdir(parents=True, exist_ok=True)
#                         shutil.copy2(child, target_child)

#     return {
#         "version": version_number,
#         "name": snapshot_name,
#         "path": snapshot_path,
#         "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         "label": label,
#     }


# def list_snapshots(snapshot_root: str = "snapshots") -> List[Dict[str, object]]:
#     snapshot_root_path = Path(snapshot_root)
#     if not snapshot_root_path.exists():
#         return []

#     snapshots = []
#     for item in sorted(snapshot_root_path.iterdir(), key=lambda p: p.name):
#         if item.is_dir() and item.name.startswith("snapshot_"):
#             parts = item.name.split("_")
#             version = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
#             snapshots.append({
#                 "version": version,
#                 "name": item.name,
#                 "path": item,
#                 "created_at": datetime.fromtimestamp(item.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
#             })
#     return snapshots


# def rollback_snapshot(version: int, target_dir: str = "test_files", snapshot_root: str = "snapshots") -> bool:
#     snapshot_root_path = Path(snapshot_root)
#     if not snapshot_root_path.exists():
#         return False

#     snapshot_match = None
#     for item in snapshot_root_path.iterdir():
#         if item.is_dir() and item.name.startswith("snapshot_"):
#             try:
#                 snap_version = int(item.name.split("_")[1])
#             except ValueError:
#                 continue
#             if snap_version == version:
#                 snapshot_match = item
#                 break

#     if snapshot_match is None:
#         return False

#     target_path = Path(target_dir)
#     target_path.mkdir(parents=True, exist_ok=True)

#     for existing in target_path.iterdir():
#         if existing.is_file():
#             existing.unlink()
#         elif existing.is_dir():
#             shutil.rmtree(existing)

#     for item in snapshot_match.iterdir():
#         if item.is_file():
#             shutil.copy2(item, target_path / item.name)
#         elif item.is_dir():
#             dest_dir = target_path / item.name
#             dest_dir.mkdir(parents=True, exist_ok=True)
#             for child in item.rglob("*"):
#                 if child.is_file():
#                     rel = child.relative_to(item)
#                     target_child = dest_dir / rel
#                     target_child.parent.mkdir(parents=True, exist_ok=True)
#                     shutil.copy2(child, target_child)

#     return True
# def delete_snapshot(version: int, snapshot_root: str = "snapshots") -> bool:
#     snapshot_root_path = Path(snapshot_root)
#     if not snapshot_root_path.exists():
#         return False

#     for item in snapshot_root_path.iterdir():
#         if item.is_dir() and item.name.startswith("snapshot_"):
#             try:
#                 snap_version = int(item.name.split("_")[1])
#             except ValueError:
#                 continue
#             if snap_version == version:
#                 shutil.rmtree(item)
#                 return True
#     return False

import hashlib
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


# ဖိုင်တစ်ခု၏ SHA-256 Hash ကို တွက်ထုတ်ပေးသည့် Function
def calculate_sha256(filepath: Path) -> str:
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def create_snapshot(target_dir: str = "test_files", snapshot_root: str = "snapshots", label: str = "") -> Dict[str, object]:
    target_path = Path(target_dir)
    snapshot_root_path = Path(snapshot_root)
    snapshot_root_path.mkdir(parents=True, exist_ok=True)

    versions = [p for p in snapshot_root_path.iterdir() if p.is_dir() and p.name.startswith("snapshot_")]
    version_number = len(versions) + 1

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    snapshot_name = f"snapshot_{version_number:03d}_{timestamp}"
    if label:
        snapshot_name = f"{snapshot_name}_{label.replace(' ', '_')}"

    snapshot_path = snapshot_root_path / snapshot_name
    snapshot_path.mkdir(parents=True, exist_ok=True)

    hashes = {}

    if target_path.exists():
        for item in target_path.rglob("*"):
            if item.is_file():
                rel = item.relative_to(target_path)
                target_child = snapshot_path / rel
                target_child.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target_child)

                # Snapshot ရိုက်စဉ် SHA-256 Hash တွက်မှတ်ထားခြင်း
                file_hash = calculate_sha256(target_child)
                hashes[str(rel)] = file_hash

    return {
        "version": version_number,
        "name": snapshot_name,
        "path": snapshot_path,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "label": label,
        "hashes": hashes,
    }


def list_snapshots(snapshot_root: str = "snapshots") -> List[Dict[str, object]]:
    snapshot_root_path = Path(snapshot_root)
    if not snapshot_root_path.exists():
        return []

    snapshots = []
    for item in sorted(snapshot_root_path.iterdir(), key=lambda p: p.name):
        if item.is_dir() and item.name.startswith("snapshot_"):
            parts = item.name.split("_")
            version = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
            snapshots.append({
                "version": version,
                "name": item.name,
                "path": item,
                "created_at": datetime.fromtimestamp(item.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            })
    return snapshots


def rollback_snapshot(version: int, target_dir: str = "test_files", snapshot_root: str = "snapshots") -> Dict[str, object]:
    snapshot_root_path = Path(snapshot_root)
    if not snapshot_root_path.exists():
        return {"success": False, "message": "Snapshot root directory not found."}

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
        return {"success": False, "message": f"Snapshot version {version} not found."}

    target_path = Path(target_dir)
    target_path.mkdir(parents=True, exist_ok=True)

    # test_files ထဲက Ransomware ခတ်ထားသော/ပျက်စီးနေသော ဖိုင်များကို ရှင်းထုတ်ခြင်း
    for existing in target_path.iterdir():
        if existing.is_file():
            existing.unlink()
        elif existing.is_dir():
            shutil.rmtree(existing)

    verified_files = 0
    hash_logs = []

    # Snapshot ထဲမှ မူရင်း ဖိုင်များကို ပြန်လည် Restoration လုပ်ခြင်းနှင့် SHA-256 တိုက်စစ်ခြင်း
    for item in snapshot_match.rglob("*"):
        if item.is_file():
            rel = item.relative_to(snapshot_match)
            target_child = target_path / rel
            target_child.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target_child)

            # Restore လုပ်ပြီးသော ဖိုင်နှင့် မူရင်း Snapshot ဖိုင်တို့၏ SHA-256 တိုက်စစ်ခြင်း
            original_hash = calculate_sha256(item)
            restored_hash = calculate_sha256(target_child)

            if original_hash == restored_hash:
                verified_files += 1
                hash_logs.append(f" {rel.name}: SHA-256 Verified ({original_hash[:10]}...)")
            else:
                hash_logs.append(f" {rel.name}: Hash Mismatch!")

    return {
        "success": True,
        "verified_count": verified_files,
        "logs": "\n".join(hash_logs),
    }


def delete_snapshot(version: int, snapshot_root: str = "snapshots") -> bool:
    snapshot_root_path = Path(snapshot_root)
    if not snapshot_root_path.exists():
        return False

    for item in snapshot_root_path.iterdir():
        if item.is_dir() and item.name.startswith("snapshot_"):
            try:
                snap_version = int(item.name.split("_")[1])
            except ValueError:
                continue
            if snap_version == version:
                shutil.rmtree(item)
                return True
    return False