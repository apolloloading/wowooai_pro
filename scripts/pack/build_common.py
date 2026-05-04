#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint:disable=too-many-statements
"""
Create a temporary conda env, install wowooai from a wheel, run conda-pack.
Used by build_macos.sh and build_win.ps1. Run from repo root.
"""
from __future__ import annotations

import argparse
import os
import random
import string
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ENV_PREFIX = "wowooai_pack_"

# Packages affected by conda-unpack bug on Windows (conda-pack Issue #154)
# conda-unpack modifies Python source files to replace path prefixes, but uses
# simple byte replacement without considering Python syntax. This corrupts
# string literals containing backslash escapes, causing SyntaxError.
# Example: "\\\\?\\" (correct) -> "\\" (SyntaxError: unterminated string)
# Solution: After conda-unpack, reinstall these packages to restore correct files
# See: issue.md and https://github.com/conda/conda-pack/issues/154
CONDA_UNPACK_AFFECTED_PACKAGES = [
    "huggingface_hub",  # file_download.py, _local_folder.py use Windows long path prefix
    "discord.py",       # ARG_NAME_SUBREGEX contains \\?\* which gets corrupted
]


def _conda_exe() -> str:
    """Resolve conda executable (required on Windows where 'conda' is a batch)."""
    exe = os.environ.get("CONDA_EXE")
    if exe:
        return exe
    return "conda"


def _run(
    cmd: list[str],
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
) -> None:
    """Run command with optional environment variable overrides.

    Always sets PYTHONNOUSERSITE=1 to prevent pip from seeing packages in
    ~/.local/lib/pythonX.Y/site-packages. If pip sees a package there as
    "already satisfied", it skips installing it into the conda env, and
    conda-pack then ships an env that's missing those packages.

    See packaging.md §8.1 for the full root-cause analysis.
    """
    run_env = os.environ.copy()
    # Hard-disable user site-packages for ALL subprocess calls (pip, conda run,
    # conda-pack). This is critical: pip's "already satisfied" check inspects
    # sys.path which includes ~/.local unless this var is set.
    run_env["PYTHONNOUSERSITE"] = "1"
    if env:
        run_env.update(env)
    subprocess.run(cmd, cwd=cwd or REPO_ROOT, env=run_env, check=True)


def _pick_wheel(wheel_arg: str | None) -> Path:
    if wheel_arg:
        wheel_path = Path(wheel_arg).expanduser()
        if not wheel_path.is_absolute():
            wheel_path = (REPO_ROOT / wheel_path).resolve()
        if not wheel_path.exists():
            raise FileNotFoundError(f"Wheel not found: {wheel_path}")
        return wheel_path

    wheels = sorted(
        (REPO_ROOT / "dist").glob("wowooai-*.whl"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not wheels:
        raise FileNotFoundError(
            "No wheel found in dist/. Run: bash scripts/wheel_build.sh",
        )
    return wheels[0]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Conda-pack wowooai (temp env).",
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="Output archive path (e.g. .tar.gz)",
    )
    parser.add_argument(
        "--format",
        "-f",
        default="infer",
        choices=["infer", "zip", "tar.gz", "tgz"],
        help="Archive format (default: infer from --output extension)",
    )
    parser.add_argument(
        "--python",
        default="3.10",
        help="Python version for conda env (default: 3.10)",
    )
    parser.add_argument(
        "--wheel",
        default=None,
        help=(
            "Wheel path to install. If omitted, pick the newest "
            "dist/wowooai-*.whl."
        ),
    )
    parser.add_argument(
        "--extras",
        default="desktop",
        help=(
            "Package extras to install from the wheel "
            "(default: desktop; use full for local/whisper dependencies)."
        ),
    )
    parser.add_argument(
        "--cache-wheels",
        action="store_true",
        help=(
            "Download wheels for packages affected by conda-unpack bug. "
            "Cached to .cache/conda_unpack_wheels/ for later reinstall."
        ),
    )
    args = parser.parse_args()
    out_path = Path(args.output).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    wheel_path = _pick_wheel(args.wheel)
    wheel_uri = wheel_path.resolve().as_uri()
    env_name = (
        f"{ENV_PREFIX}{''.join(random.choices(string.ascii_lowercase, k=8))}"
    )

    conda = _conda_exe()
    try:
        _run(
            [
                conda,
                "create",
                "-n",
                env_name,
                f"python={args.python}",
                "pip",
                "-y",
            ],
        )
        _run(
            [
                conda,
                "run",
                "-n",
                env_name,
                "python",
                "-m",
                "pip",
                "install",
                "--no-user",
                "--upgrade",
                "pip",
            ],
        )

        # Install Node.js into the conda env so that the packaged .app ships
        # its own node/npm/npx. MCP stdio servers (e.g. tavily-mcp) use
        # "npx -y <pkg>" to launch; without a bundled npx the GUI app fails
        # because macOS launchd PATH doesn't include user-installed Node.
        # See packaging.md §10 for the full root-cause analysis.
        print("Installing Node.js into conda env (required for MCP stdio)...")
        _run(
            [
                conda,
                "install",
                "-n",
                env_name,
                "nodejs",
                "-y",
            ],
        )

        # Install wowooai with all dependencies
        # Scope CMAKE_ARGS to this specific command to avoid affecting other
        # CMake-based packages. Only set if we need to compile from source.
        install_env = {}

        # --no-user: prevents pip from skipping packages that exist in
        # ~/.local/lib/pythonX.Y/site-packages (which would cause conda-pack
        # to ship an env missing those deps). See packaging.md §8.1.
        _run(
            [
                conda,
                "run",
                "-n",
                env_name,
                "python",
                "-m",
                "pip",
                "install",
                "--no-user",
                f"wowooai[{args.extras}] @ {wheel_uri}",
            ],
            env=install_env,
        )

        # Verify no broken requirements remain (catches ~/.local leaks early).
        # If any required package is still missing, abort the build now rather
        # than ship a broken DMG.
        print("Verifying installed environment has no broken requirements...")
        check_proc = subprocess.run(
            [
                conda,
                "run",
                "-n",
                env_name,
                "python",
                "-m",
                "pip",
                "check",
            ],
            cwd=REPO_ROOT,
            env={**os.environ, "PYTHONNOUSERSITE": "1"},
            capture_output=True,
            text=True,
            check=False,
        )
        check_output = (check_proc.stdout or "") + (check_proc.stderr or "")
        # pip check exits non-zero if there are broken requirements.
        # Some "Requirement already satisfied" style messages are fine; the
        # actual breakage signal is "is not installed" or "has requirement".
        if (
            "is not installed" in check_output
            or "has requirement" in check_output
        ):
            print(check_output)
            raise RuntimeError(
                "pip check reported broken requirements after install. "
                "This usually means packages leaked from ~/.local. "
                "See packaging.md §8.1 for diagnosis.",
            )
        print("pip check passed (no broken requirements).")
        print("Verifying certifi is installed (required for SSL)...")
        _run(
            [
                conda,
                "run",
                "-n",
                env_name,
                "python",
                "-c",
                "import certifi; print(f'certifi OK: {certifi.where()}')",
            ],
        )
        # Verify Node.js / npx is available inside the conda env.
        # MCP stdio servers (tavily-mcp etc.) need npx at runtime.
        print("Verifying npx is available (required for MCP stdio)...")
        _run(
            [
                conda,
                "run",
                "-n",
                env_name,
                "npx",
                "--version",
            ],
        )
        if args.cache_wheels:
            # Store outside dist/ to avoid being deleted by wheel_build cleanup
            wheels_cache = REPO_ROOT / ".cache" / "conda_unpack_wheels"
            wheels_cache.mkdir(parents=True, exist_ok=True)
            print(
                f"Caching wheels for conda-unpack bug workaround to "
                f"{wheels_cache}",
            )
            _run(
                [
                    conda,
                    "run",
                    "-n",
                    env_name,
                    "python",
                    "-m",
                    "pip",
                    "download",
                    *CONDA_UNPACK_AFFECTED_PACKAGES,
                    "-d",
                    str(wheels_cache),
                ],
            )
        _run(
            [
                conda,
                "run",
                "-n",
                env_name,
                conda,
                "install",
                "-y",
                "conda-pack",
            ],
        )
        if out_path.exists():
            out_path.unlink()
        pack_cmd = [
            conda,
            "run",
            "-n",
            env_name,
            "conda-pack",
            "-n",
            env_name,
            "-o",
            str(out_path),
            "-f",
        ]
        if args.format != "infer":
            pack_cmd.extend(["--format", args.format])
        _run(pack_cmd)
        print(f"Packed to {out_path}")
    finally:
        try:
            _run([conda, "env", "remove", "-n", env_name, "-y"])
        except Exception as e:
            print(f"Warning: Failed to remove temp env {env_name}: {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
