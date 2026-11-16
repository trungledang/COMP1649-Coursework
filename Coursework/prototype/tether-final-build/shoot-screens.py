"""Screenshot every exported page of the Tether prototype with headless Edge.

The exported Axure HTML centres the 430 px phone frame in the browser window, so
the shot is taken at 520 px wide and then cropped to the frame itself. This
gives clean, report-ready images of the *current* prototype (the ones in
Coursework/prototype/demo/ were taken on 2026-11-02 against an older build).

Usage:  python shoot-screens.py <export-dir> <out-dir>
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
WIN_W, WIN_H = 520, 960
FRAME_W = 430

PAGES = [
    ("00_welcome", "01 Welcome"),
    ("01_log_in", "02 Log in"),
    ("02_create_account", "03 Create account"),
    ("03_set_your_pace", "04 Set your pace"),
    ("04_today", "05 Today"),
    ("05_add_assignment", "06 Add assignment"),
    ("06_check_requirements", "07 Check requirements"),
    ("07_your_plan", "08 Your plan"),
    ("08_study_time", "09 Study time"),
    ("09_study_time_saved", "10 Study time saved"),
    ("10_your_space", "11 Your space"),
    ("01_my_study_desk", "12 My study desk"),
    ("02_continue_your_work", "13 Continue your work"),
    ("03_when_you_are_stuck", "14 When you are stuck"),
    ("04_leave_a_thread", "15 Leave a thread"),
    ("05_ready_to_return", "16 Ready to return"),
    ("06_step_complete", "17 Step complete"),
]


def shoot(html, out_png, width=WIN_W, height=WIN_H):
    subprocess.run(
        [EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         "--force-device-scale-factor=1", f"--window-size={width},{height}",
         f"--screenshot={out_png}", html],
        check=False, capture_output=True, timeout=120)
    return Path(out_png).exists()


def crop_to_frame(png):
    im = Image.open(png)
    left = (im.width - FRAME_W) // 2
    if left <= 0:
        return im.width, im.height
    im = im.crop((left, 0, left + FRAME_W, min(im.height, 960)))
    im.save(png)
    return im.width, im.height


def main():
    exp = Path(sys.argv[1])
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    for slug, label in PAGES:
        html = exp / f"{slug}.html"
        if not html.exists():
            print("missing", html)
            continue
        png = out / f"{slug}.png"
        uri = html.resolve().as_uri()
        if not shoot(uri, png):
            print("FAILED", slug)
            continue
        w, h = crop_to_frame(png)
        print(f"  {slug:24} -> {png.name} {w}x{h}")


if __name__ == "__main__":
    main()
