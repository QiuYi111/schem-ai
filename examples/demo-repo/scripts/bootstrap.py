from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
import urllib.request
import venv
from pathlib import Path

LIGHTPANDA_URL = os.environ.get(
    "LIGHTPANDA_URL",
    "https://github.com/lightpanda-io/browser/releases/download/nightly/lightpanda-aarch64-macos",
)
PDF_TO_MARKDOWN_REPO = os.environ.get(
    "PDF_TO_MARKDOWN_REPO",
    "https://github.com/iamarunbrahma/pdf-to-markdown.git",
)


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def tools_root(root: Path) -> Path:
    return root / ".tools"


def tools_bin_dir(root: Path) -> Path:
    return tools_root(root) / "bin"


def local_which(tool: str, root: Path) -> str | None:
    search_path = os.pathsep.join([str(tools_bin_dir(root)), os.environ.get("PATH", "")])
    return shutil.which(tool, path=search_path)


def run(cmd: list[str], root: Path, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=cwd or root,
        capture_output=True,
        text=True,
        check=False,
    )


def print_result(result: subprocess.CompletedProcess[str]) -> None:
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())


def ensure_mac_host() -> bool:
    if platform.system() != "Darwin":
        print(f"Unsupported host: {platform.system()}. This bootstrap script currently supports macOS only.")
        return False
    return True


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def install_lightpanda(root: Path) -> bool:
    existing = local_which("lightpanda", root) or shutil.which("lightpanda")
    if existing:
        print(f"- lightpanda: {existing}")
        return True

    print(f"- lightpanda: downloading {LIGHTPANDA_URL}")
    target = tools_bin_dir(root) / "lightpanda"
    ensure_dir(target.parent)
    try:
        with urllib.request.urlopen(LIGHTPANDA_URL) as response:
            target.write_bytes(response.read())
        os.chmod(target, 0o755)
    except Exception as exc:
        print(f"  Failed to install Lightpanda: {exc}")
        return False

    print(f"  Installed Lightpanda to {target}")
    return True


def install_pdf_to_markdown(root: Path) -> bool:
    existing = local_which("pdf-to-markdown", root) or shutil.which("pdf-to-markdown")
    if existing:
        print(f"- pdf-to-markdown: {existing}")
        return True

    repo_dir = tools_root(root) / "pdf-to-markdown"
    if not repo_dir.exists():
        print(f"- pdf-to-markdown: cloning {PDF_TO_MARKDOWN_REPO}")
        clone = run(["git", "clone", "--depth", "1", PDF_TO_MARKDOWN_REPO, str(repo_dir)], root)
        print_result(clone)
        if clone.returncode != 0:
            return False
    else:
        print(f"- pdf-to-markdown: updating {repo_dir}")
        pull = run(["git", "pull", "--ff-only"], root, cwd=repo_dir)
        print_result(pull)
        if pull.returncode != 0:
            return False

    venv_dir = repo_dir / ".venv"
    if not venv_dir.exists():
        print(f"  Creating virtualenv at {venv_dir}")
        venv.create(venv_dir, with_pip=True)

    python_bin = venv_dir / "bin" / "python"
    pip_upgrade = run([str(python_bin), "-m", "pip", "install", "--upgrade", "pip"], root, cwd=repo_dir)
    print_result(pip_upgrade)
    if pip_upgrade.returncode != 0:
        return False

    requirements = repo_dir / "requirements.txt"
    if not requirements.exists():
        print(f"  Missing requirements file: {requirements}")
        return False

    install = run([str(python_bin), "-m", "pip", "install", "-r", str(requirements)], root, cwd=repo_dir)
    print_result(install)
    if install.returncode != 0:
        return False

    target = tools_bin_dir(root) / "pdf-to-markdown"
    ensure_dir(target.parent)
    target.write_text(
        "#!/usr/bin/env sh\n"
        f'exec "{python_bin}" "{repo_dir / "extract.py"}" "$@"\n',
        encoding="utf-8",
        newline="\n",
    )
    os.chmod(target, 0o755)
    print(f"  Installed pdf-to-markdown wrapper to {target}")
    return True


def main() -> int:
    root = project_root()
    checks = {
        "python": shutil.which("python") or sys.executable,
        "git": shutil.which("git"),
        "make": shutil.which("make"),
    }
    print("Environment check:")
    for name, value in checks.items():
        status = value if value else "missing"
        print(f"- {name}: {status}")
    if not checks["python"] or not checks["git"]:
        print("Missing required tools: python and git are mandatory.")
        return 1
    if not checks["make"]:
        print("Notice: make is optional. You can still run the Python scripts directly.")
    if not ensure_mac_host():
        return 1

    print("Installing project-local dependencies:")
    ok_lightpanda = install_lightpanda(root)
    ok_pdf = install_pdf_to_markdown(root)
    print(f"Local tool bin directory: {tools_bin_dir(root)}")
    print("Add this directory to PATH if you want to invoke the installed tools directly.")
    return 0 if ok_lightpanda and ok_pdf else 1


if __name__ == "__main__":
    sys.exit(main())
