"""Polish pass on the Tether prototype (2026-11-16), round 2.

Fixes applied here
------------------
1. The avatar label was set to the literal string "[[TetherName]]" while probing
   whether Axure parses inline expressions through the bridge. It does not: the
   bridge builds plain rich-text runs, so the prototype rendered the brackets.
   The avatar goes back to a clean "A" and the dynamic initial is documented as
   a 2-minute manual step in the Axure editor (the editor does parse [[...]]).

2. On 04 Today the profile avatar overlaps the page title: the title box is
   (273,74) 129 px wide and right aligned, so "My study desk" runs from ~322 to
   402 px while the avatar circle occupies 360-400 px. The title box is moved
   left to (223,74) so the two never collide.

3. The whole prototype is saved and exported with Axure's own generator, and
   every page is re-checked for a 430 px adaptive view.
"""
import re
import shutil
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent / "bridge-research" / "native-cli"
sys.path.insert(0, str(KIT))

APP = r"C:\Program Files (x86)\Axure\Axure RP 11\AxureRP11.exe"
HERE = Path(__file__).resolve().parent
PROTO = HERE.parent
WORK_RP = PROTO / "tether-build-2026-11-16.rp"
EXPORT_DIR = HERE / "export-verify-2026-11-16"

import axure_cli as a  # noqa: E402

TODAY = "5f19db87-3d67-4040-aae3-25f9e559466b"
AVATAR_INITIAL = "47992a39-f2c1-4848-872b-439b74a0b1ce"


def call(op, timeout=60, **kw):
    out = a.request(dict(op=op, **kw), timeout)
    if not out.get("ok"):
        raise RuntimeError(f"{op} failed: {out.get('error')}")
    return out.get("result")


def ensure_launch():
    try:
        a.endpoint()
        return
    except RuntimeError:
        pass
    if not WORK_RP.exists():
        shutil.copy2(PROTO / "tether-revision-2026-11-09.rp", WORK_RP)
    out = a.launch(project=str(WORK_RP), app=APP)
    if not out.get("ok"):
        raise RuntimeError(f"launch failed: {out}")


def find(pred):
    for w in call("widget.list"):
        if pred(w):
            return w
    return None


def main():
    ensure_launch()
    call("page.open", id=TODAY)

    # 1. avatar back to a plain letter
    av = find(lambda w: w["id"] == AVATAR_INITIAL)
    if av and av.get("text") != "A":
        call("widget.text", id=AVATAR_INITIAL, text="A")
        print("avatar initial -> 'A'")

    # 2. title box moved left so it cannot collide with the avatar
    title = find(lambda w: w.get("text") == "My study desk" and w["bounds"]["y"] == 74)
    if title:
        b = title["bounds"]
        if b["x"] > 240:
            res = call("widget.bounds", id=title["id"], x=223)
            print(f"title box moved {b['x']} -> {res['after']['bounds']['x']}")

    # 3. save + native export
    print("saved:", call("project.save", path=str(WORK_RP)))
    if EXPORT_DIR.exists():
        shutil.rmtree(EXPORT_DIR)
    EXPORT_DIR.mkdir(parents=True)
    print("exported:", call("export.html", output=str(EXPORT_DIR), timeout=300))

    # 4. verify
    files = EXPORT_DIR / "files"
    bad = []
    for pg in sorted(p.name for p in files.iterdir() if p.is_dir()):
        djs = (files / pg / "data.js").read_text(encoding="utf-8", errors="replace")
        css = (files / pg / "styles.css").read_text(encoding="utf-8", errors="replace")
        m = re.search(r"defaultAdaptiveView.{0,140}?m=(\d+)", djs, re.S)
        c = re.search(r"body \{.{0,220}?width:(-?\d+)px", css, re.S)
        native, body = int(m.group(1)) if m else -1, int(c.group(1)) if c else -1
        if not (native == 430 and body == 430):
            bad.append((pg, native, body))
    print("canvas:", "ALL 17 AT 430px" if not bad else f"PROBLEMS {bad}")


if __name__ == "__main__":
    main()
