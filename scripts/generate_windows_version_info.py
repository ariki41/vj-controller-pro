from __future__ import annotations

import argparse
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VERSION_FILE = PROJECT_ROOT / "VERSION"
DEFAULT_OUTPUT_FILE = PROJECT_ROOT / "build" / "windows-version-info.txt"
SEMVER_PATTERN = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)


def parse_version(version: str) -> tuple[int, int, int, int]:
    match = SEMVER_PATTERN.fullmatch(version)
    if match is None:
        raise ValueError(f"VERSION must be a semantic version: {version!r}")

    core = version.split("-", 1)[0].split("+", 1)[0]
    return (*map(int, core.split(".")), 0)


def render_version_info(version: str) -> str:
    version_tuple = parse_version(version)
    return f"""VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={version_tuple},
    prodvers={version_tuple},
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        '040904B0',
        [
          StringStruct('CompanyName', 'ariki41'),
          StringStruct('FileDescription', 'VJ Controller Pro'),
          StringStruct('FileVersion', '{version}'),
          StringStruct('InternalName', 'vj-controller-pro'),
          StringStruct('LegalCopyright', 'Copyright (c) 2026 ariki41'),
          StringStruct('OriginalFilename', 'vj-controller-pro.exe'),
          StringStruct('ProductName', 'VJ Controller Pro'),
          StringStruct('ProductVersion', '{version}')
        ]
      )
    ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
"""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate the PyInstaller Windows version resource from VERSION."
    )
    parser.add_argument("--version-file", type=Path, default=DEFAULT_VERSION_FILE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_FILE)
    args = parser.parse_args()

    version = args.version_file.read_text(encoding="utf-8").strip()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_version_info(version), encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
