"""Build the self-contained skill ZIP accepted by the OpenAI submission portal."""

import argparse
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    skill = (root / "skills/social-posting/SKILL.md").read_text(encoding="utf-8")
    skill = skill.replace("../../scripts/upload_media.py", "scripts/upload_media.py")
    with ZipFile(args.output, "w", ZIP_DEFLATED) as archive:
        archive.writestr("SKILL.md", skill)
        archive.write(root / "scripts/upload_media.py", "scripts/upload_media.py")
    print(f"Created {args.output}")


if __name__ == "__main__":
    main()
