"""Fix the 1001 px adaptive-view width in the Tether prototype (2026-11-16).

Problem
-------
The 2026-11-16 Antigravity session found that several pages had three layers of
stacked buttons. Instead of deleting the superseded widgets it *parked* them at
(1000,1000). Axure derives the adaptive-view width from the widget bounding
box, so 5 pages became 1001 px wide. The exported HTML was then hand-patched
(`body{width:-4570px}` -> `body{width:430px}`) so the demo still looked right.

That is exactly what tools/axure-ai/README.md forbids ("never hand-edit an
exported HTML file to fake behaviour") and it leaves the submitted .rp with a
broken canvas: a marker who opens the .rp - or exports it themselves - gets the
1001 px layout, not the 430 px one that was verified.

This script
-----------
1. copies the canonical .rp to a working copy,
2. verifies for every parked widget that a live widget on the same page
   already covers the same interaction cases (so nothing is lost),
3. deletes the parked widgets with Axure's native editor delete
   (undoable, same transaction model as the rest of the bridge),
4. saves and exports with Axure's own HTML generator - no hand edits,
5. verifies from the exported data.js that all 17 pages report a 430 px
   adaptive view and that the CSS body width matches it.

Usage:  python fix-canvas-width.py fix
"""
import json
import os
import re
import shutil
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent / "bridge-research" / "native-cli"
sys.path.insert(0, str(KIT))

APP = os.environ.get("AXURE_APP", r"C:\Program Files (x86)\Axure\Axure RP 11\AxureRP11.exe")
PROTO = Path(__file__).resolve().parent.parent
WORK_RP = PROTO / "tether-build-2026-11-16.rp"
CANON_RP = PROTO / "tether-revision-2026-11-09.rp"
EXPORT_DIR = Path(__file__).resolve().parent / "export-verify-2026-11-16"

BROKEN_PAGES = [
    "07 Your plan",
    "02 Continue your work",
    "03 When you are stuck",
    "04 Leave a thread",
    "06 Check requirements",
]

# Parked widgets whose live replacement has differently named cases, verified by
# reading both interaction maps by hand (see notes below).
#   04 Leave a thread / hit_save
#     live: hit_save_with_variables
#     -> "Missing position"  identical setText on widget 5b194b6d...
#     -> "Missing next move" identical setText on widget 5b194b6d...
#     -> old "Finish"          navigate -> page e4aac2f0 (05 Ready to return)
#     -> new "Save and continue" same navigate + two SetGlobalVariableValue
#        writes (TetherWhere / TetherNext) before it.
#     The live widget is a strict superset, so the parked one is dead weight.
VERIFIED_SUPERSEDED = {
    ("04 Leave a thread", "hit_save"): "hit_save_with_variables",
}

import axure_cli as a  # noqa: E402


def call(op, timeout=60, **kw):
    out = a.request(dict(op=op, **kw), timeout)
    if not out.get("ok"):
        raise RuntimeError(f"{op} failed: {out.get('error')}")
    return out.get("result")


def pages():
    flat = []

    def walk(nodes):
        for n in nodes or []:
            flat.append(n)
            walk(n.get("Children"))

    walk(call("page.list").get("pages"))
    return flat


def page_id(name):
    for p in pages():
        if p.get("Name") == name:
            return p["Id"]
    raise KeyError(name)


def open_page(name):
    call("page.open", id=page_id(name))


def widgets():
    return call("widget.list")


def cases_of(widget_id):
    ix = call("interaction.get", id=widget_id)
    out = set()
    for ev in ix.get("events") or []:
        for case in ev.get("cases") or []:
            if case.get("name"):
                out.add(case["name"])
    return out


def is_parked(w):
    b = w["bounds"]
    return b["x"] > 431 or b["x"] < -1


def verify_and_delete():
    report = []
    for target in BROKEN_PAGES:
        open_page(target)
        ws = widgets()
        parked = [w for w in ws if is_parked(w)]
        live = [w for w in ws if not is_parked(w)]
        live_cases = {}
        for w in live:
            live_cases[w["id"]] = cases_of(w["id"])
        print(f"\n== {target}: {len(ws)} widgets, {len(parked)} parked")
        for w in parked:
            need = cases_of(w["id"])
            cover = [lid for lid, cs in live_cases.items() if need and need <= cs]
            live_name = VERIFIED_SUPERSEDED.get((target, w["name"]))
            if not cover and live_name:
                cover = [lid for lid, cs in live_cases.items()
                         if any(w2["name"] == live_name and w2["id"] == lid for w2 in live)]
            if need and not cover:
                print(f"   !! KEEP {w['name']}: no live widget covers {sorted(need)}")
                report.append((target, w["name"], "kept"))
                continue
            res = call("widget.delete", id=w["id"])
            print(f"   deleted {w['name']:26} cases={sorted(need)} covered_by={len(cover)}"
                  f"{' (verified superset)' if live_name else ''}")
            report.append((target, w["name"], "deleted"))
    return report


def save_and_export():
    res = call("project.save", path=str(WORK_RP))
    print("\nsaved:", res)
    if EXPORT_DIR.exists():
        shutil.rmtree(EXPORT_DIR)
    EXPORT_DIR.mkdir(parents=True)
    out = call("export.html", output=str(EXPORT_DIR), timeout=300)
    print("exported:", out)


def verify_export():
    files = EXPORT_DIR / "files"
    bad = []
    for pg in sorted(p.name for p in files.iterdir() if p.is_dir()):
        djs = (files / pg / "data.js").read_text(encoding="utf-8", errors="replace")
        m = re.search(r"defaultAdaptiveView.{0,140}?m=(\d+)", djs, re.S)
        css = (files / pg / "styles.css").read_text(encoding="utf-8", errors="replace")
        c = re.search(r"body \{.{0,220}?width:(-?\d+)px", css, re.S)
        native = int(m.group(1)) if m else -1
        body = int(c.group(1)) if c else -1
        ok = native == 430 and body == 430
        print(f"  {pg:24} native={native:<6} css_body={body:<6} {'OK' if ok else '<<< PROBLEM'}")
        if not ok:
            bad.append((pg, native, body))
    return bad


def main():
    print("launching Axure with a fresh working copy ...")
    if WORK_RP.exists():
        WORK_RP.unlink()
    shutil.copy2(CANON_RP, WORK_RP)
    out = a.launch(project=str(WORK_RP), app=APP)
    if not out.get("ok"):
        raise SystemExit(f"launch failed: {out}")
    try:
        verify_and_delete()
        save_and_export()
        print("\n=== export verification ===")
        bad = verify_export()
        print("\nRESULT:", "ALL 17 PAGES AT 430px" if not bad else f"PROBLEMS: {bad}")
    finally:
        try:
            call("project.close")
        except Exception as exc:  # noqa: BLE001
            print("close failed:", exc)


if __name__ == "__main__":
    main()
