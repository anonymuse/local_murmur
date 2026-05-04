from __future__ import annotations

import tempfile
from pathlib import Path


def get_temp_root(temp_dir: Path | None) -> Path:
    root = temp_dir if temp_dir is not None else Path(tempfile.gettempdir()) / "local-murmur"
    root.mkdir(parents=True, exist_ok=True)
    return root


def stage_upload_bytes(
    *,
    root: Path,
    filename: str,
    contents: bytes,
) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    suffix = Path(filename).suffix or ".upload"
    with tempfile.NamedTemporaryFile(
        delete=False,
        dir=root,
        prefix="upload-",
        suffix=suffix,
    ) as handle:
        handle.write(contents)
        return Path(handle.name)


def cleanup_path(path: Path | None) -> None:
    if path is None:
        return
    try:
        path.unlink()
    except FileNotFoundError:
        pass
