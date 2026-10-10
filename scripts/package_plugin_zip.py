"""Build the complete plugin ZIP for the OpenAI Platform plugin portal.

The portal requires the package `name` to match the existing plugin
(`app-6aa12df9031081918791b12e783d8ae4`). The repository keeps `so-me-studio`
so local Codex installs keep their identity; only the ZIP gets the portal name.
"""

import argparse
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

PORTAL_NAME = "app-6aa12df9031081918791b12e783d8ae4"
FILES = [".mcp.json", "LICENSE", "README.md", "scripts/upload_media.py"]
DIRS = ["assets", "skills"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--name", default=PORTAL_NAME)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    manifest["name"] = args.name
    with ZipFile(args.output, "w", ZIP_DEFLATED) as archive:
        archive.writestr(".codex-plugin/plugin.json", json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
        for name in FILES:
            archive.write(root / name, name)
        for directory in DIRS:
            for path in sorted((root / directory).rglob("*")):
                if path.is_file() and "__pycache__" not in path.parts and path.name != ".DS_Store":
                    archive.write(path, path.relative_to(root).as_posix())
    print(f"Created {args.output} ({manifest['name']} {manifest['version']})")


if __name__ == "__main__":
    main()
