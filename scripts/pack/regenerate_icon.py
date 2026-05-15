#!/usr/bin/env python3
"""Generate icon.icns + icon.ico with Apple HIG safe-area padding.

Artwork (rounded square + 'W' mark + dot) occupies ~80% of canvas;
each edge has ~10% transparent padding so the icon visually matches
Apple system apps in the Dock / Finder.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parents[2]
ASSETS = REPO / "scripts" / "pack" / "assets"
OUT_ICNS = ASSETS / "icon.icns"
OUT_ICO = ASSETS / "icon.ico"

BRAND_BLUE = (37, 99, 235, 255)   # #2563EB
WHITE = (255, 255, 255, 255)

CANVAS = 1024
ART = 824                          # 80.5% — Apple HIG macOS Big Sur+ template
PAD = (CANVAS - ART) // 2          # 100
CORNER_RADIUS_RATIO = 0.224        # corner radius / artwork width


def render_master(size: int = CANVAS) -> Image.Image:
    """Render artwork centered on a transparent canvas."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    art = ART * size // CANVAS
    pad = (size - art) // 2
    radius = int(art * CORNER_RADIUS_RATIO)

    # Rounded square background
    draw.rounded_rectangle(
        [(pad, pad), (pad + art, pad + art)],
        radius=radius,
        fill=BRAND_BLUE,
    )

    # W mark — same coordinates as favicon.svg viewBox 64x64, scaled to artwork
    def s(v: float) -> float:
        return pad + v * art / 64.0

    stroke_w = max(2, int(6 * art / 64.0))
    pts = [(s(12), s(18)), (s(22), s(48)), (s(32), s(28)), (s(42), s(48)), (s(52), s(18))]
    draw.line(pts, fill=WHITE, width=stroke_w, joint="curve")
    # Round endpoints (PIL line doesn't auto round-cap)
    cap_r = stroke_w // 2
    for x, y in pts:
        draw.ellipse(
            [(x - cap_r, y - cap_r), (x + cap_r, y + cap_r)],
            fill=WHITE,
        )

    # AI node dot at top-right of W: white halo + blue inner
    cx, cy = s(52), s(18)
    outer = 5 * art / 64.0
    inner = 2 * art / 64.0
    draw.ellipse([(cx - outer, cy - outer), (cx + outer, cy + outer)], fill=WHITE)
    draw.ellipse([(cx - inner, cy - inner), (cx + inner, cy + inner)], fill=BRAND_BLUE)

    return img


def build_iconset(master: Image.Image, work: Path) -> Path:
    iconset = work / "icon.iconset"
    iconset.mkdir(parents=True, exist_ok=True)
    sizes = [
        (16, "icon_16x16.png"),
        (32, "icon_16x16@2x.png"),
        (32, "icon_32x32.png"),
        (64, "icon_32x32@2x.png"),
        (128, "icon_128x128.png"),
        (256, "icon_128x128@2x.png"),
        (256, "icon_256x256.png"),
        (512, "icon_256x256@2x.png"),
        (512, "icon_512x512.png"),
        (1024, "icon_512x512@2x.png"),
    ]
    for px, name in sizes:
        master.resize((px, px), Image.LANCZOS).save(iconset / name, "PNG")
    return iconset


def compile_icns(iconset: Path, out: Path) -> None:
    out.unlink(missing_ok=True)
    subprocess.run(
        ["iconutil", "-c", "icns", str(iconset), "-o", str(out)],
        check=True,
    )


def write_ico(master: Image.Image, out: Path) -> None:
    out.unlink(missing_ok=True)
    sizes = [(s, s) for s in (16, 24, 32, 48, 64, 128, 256)]
    master.save(out, format="ICO", sizes=sizes)


def main() -> int:
    work = REPO / ".tmp_icon_build"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()

    master = render_master(CANVAS)
    master_png = work / "master.png"
    master.save(master_png, "PNG")
    print(f"[+] master rendered: {master_png}  {master.size}  art={ART}px pad={PAD}px")

    iconset = build_iconset(master, work)
    print(f"[+] iconset built: {iconset}")
    for p in sorted(iconset.iterdir()):
        print(f"    {p.name}")

    compile_icns(iconset, OUT_ICNS)
    print(f"[+] icns compiled: {OUT_ICNS}  ({OUT_ICNS.stat().st_size} bytes)")

    write_ico(master, OUT_ICO)
    print(f"[+] ico written:   {OUT_ICO}  ({OUT_ICO.stat().st_size} bytes)")

    shutil.rmtree(work)
    print(f"[+] cleaned: {work}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
