from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from common import resolve_project_root, run_hook_group, utc_now


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()

    project_root = resolve_project_root(args.project_root)
    design_path = project_root / "design" / "interconnect.json"
    out_dir = project_root / "render" / "schematic_output"

    hook_result = run_hook_group(
        project_root,
        "pre-render",
        {
            "HOOK_RENDER_INPUT": str(design_path),
            "HOOK_RENDER_OUTPUT_DIR": str(out_dir),
        },
    )
    if hook_result != 0:
        return hook_result

    if not design_path.exists():
        print(f"Missing design input: {design_path}")
        return 1

    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate HTML schematic
    viewer_js_path = Path(__file__).with_name("schematic_viewer.js")
    viewer_js = viewer_js_path.read_text(encoding="utf-8") if viewer_js_path.exists() else ""
    
    payload_str = design_path.read_text(encoding="utf-8-sig")
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Schematic View - {project_root.name}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body, html {{ margin: 0; padding: 0; width: 100%; height: 100%; background: #1a1a1a; color: #fff; overflow: hidden; }}
        #app {{ width: 100%; height: 100%; display: flex; flex-direction: column; }}
        header {{ padding: 15px 25px; background: #252525; border-bottom: 1px solid #333; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
        h1 {{ margin: 0; font-size: 18px; font-weight: 600; color: #00d4ff; }}
        .controls {{ display: flex; gap: 10px; color: #888; font-size: 12px; }}
        #viewer-container {{ flex: 1; position: relative; }}
        .legend {{ position: absolute; bottom: 20px; right: 20px; background: rgba(0,0,0,0.5); padding: 10px; border-radius: 4px; font-size: 11px; pointer-events: none; }}
        .legend-item {{ display: flex; align-items: center; gap: 5px; margin-bottom: 5px; }}
        .color-dot {{ width: 8px; height: 8px; border-radius: 50%; }}
    </style>
</head>
<body>
    <div id="app">
        <header>
            <h1>Schem-AI: {project_root.name}</h1>
            <div class="controls">
                <span>Scroll to Zoom</span>
                <span>•</span>
                <span>Drag to Pan</span>
                <span>•</span>
                <span>Hover Net to Highlight</span>
            </div>
        </header>
        <div id="viewer-container"></div>
        <div class="legend">
            <div class="legend-item"><div class="color-dot" style="background:#00d4ff"></div>Component</div>
            <div class="legend-item"><div class="color-dot" style="background:#ff9f43"></div>Net Label</div>
        </div>
    </div>
    <script>
        {viewer_js}
        
        const designData = {payload_str};
        document.addEventListener('DOMContentLoaded', () => {{
            new SchematicViewer('viewer-container', designData);
        }});
    </script>
</body>
</html>"""

    index_html = out_dir / "index.html"
    index_html.write_text(html_content, encoding="utf-8")

    placeholder = out_dir / "placeholder_schematic.txt"
    payload = json.loads(payload_str)
    placeholder.write_text(
        "Rendered Web Schematic\n"
        f"Generated from: {design_path.name}\n"
        f"Output file: index.html\n",
        encoding="utf-8",
    )
    log_path = project_root / "render" / "render_log.md"
    log_path.write_text(
        "\n".join(
            [
                "# Render Log",
                "",
                f"- Timestamp: {utc_now()}",
                "- Renderer: Interactive Web Renderer",
                f"- Input: {design_path.relative_to(project_root).as_posix()}",
                f"- Output: {index_html.relative_to(project_root).as_posix()}",
                "",
                "## Summary",
                f"Generated premium interactive schematic viewer at `{index_html.name}`.",
                "Utilized net labels for all component interconnections as per user requirement.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    hook_result = run_hook_group(
        project_root,
        "post-render",
        {
            "HOOK_RENDER_INPUT": str(design_path),
            "HOOK_RENDER_OUTPUT_DIR": str(out_dir),
            "HOOK_RENDER_LOG": str(log_path),
        },
    )
    if hook_result != 0:
        return hook_result

    print(f"Rendered placeholder output at {placeholder}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
