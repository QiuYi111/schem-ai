from __future__ import annotations

import sys

from common import ROOT, utc_now


def main() -> int:
    out_dir = ROOT / "render" / "schematic_output"
    out_dir.mkdir(parents=True, exist_ok=True)
    placeholder = out_dir / "placeholder_schematic.txt"
    placeholder.write_text(
        "Render placeholder\n"
        "This file stands in for a future schematic renderer output.\n",
        encoding="utf-8",
    )
    log_path = ROOT / "render" / "render_log.md"
    log_path.write_text(
        "\n".join(
            [
                "# Render Log",
                "",
                f"- Timestamp: {utc_now()}",
                "- Renderer: placeholder",
                f"- Output: {placeholder.relative_to(ROOT).as_posix()}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Rendered placeholder output at {placeholder}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
