"""Apply the remaining small prototype tasks (A + B) to the Tether prototype.

Task A - the assignment brief input needs guidance (one requirement per line).
Task B - the sign-up name is captured into the TetherName global variable so the
         prototype behaves like one coherent product instead of five demos.

Every mutation is read back and the result is verified from Axure's own HTML
export. The exported HTML is never edited by hand.

Usage:  python apply-tasks.py [avatar-text]
"""
import json
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

PAGES = {
    "05 Add assignment": "489c9fbb-efd5-48a8-a4fe-773fb46cbd7c",
    "02 Create account": "3bab9d97-8a22-4340-9240-ed5713788abc",
    "04 Today": "5f19db87-3d67-4040-aae3-25f9e559466b",
}

# --- task A ---------------------------------------------------------------
BRIEF_LABEL_ID = "d48caa75-aeb2-4b50-baa1-4daa3a04be4c"   # "What do you need to do?"
BRIEF_FIELD_ID = "0ea5fb74-62b2-4c36-ac4c-087d0a45010d"   # assignment_brief (TextArea)
BRIEF_LABEL_TEXT = "Key requirements (one per line)"
BRIEF_PLACEHOLDER = "One requirement per line, e.g. Report: 2,000-3,000 words"

# --- task B ---------------------------------------------------------------
SIGNUP_BUTTON = "3608540f-3faa-46a8-a01f-189fffdf065b"   # app_signup
SIGNUP_NAME = "952d1c18-fc44-4cc4-8d77-6774cb63309f"      # signup_name input
SIGNUP_EMAIL = "737b6731-ee7b-45ed-9c53-6d3bca2da555"     # signup_email input
SIGNUP_PASSWORD = "6ab7cee2-8519-4180-872b-ee050ec95840"  # signup_password input
SIGNUP_ERROR = "31bb5821-48f7-493e-ae12-506a292b80f7"      # error hint text
SIGNUP_TARGET = "99743f17-ab94-4419-953d-74b4e960b825"    # 03 Set your pace
AVATAR_INITIAL = "47992a39-f2c1-4848-872b-439b74a0b1ce"   # profile_avatar_initial


def call(op, timeout=60, **kw):
    out = a.request(dict(op=op, **kw), timeout)
    if not out.get("ok"):
        raise RuntimeError(f"{op} failed: {out.get('error')}")
    return out.get("result")


def open_page(name):
    call("page.open", id=PAGES[name])


def by_id(wid):
    for w in call("widget.list"):
        if w["id"] == wid:
            return w
    raise KeyError(wid)


def task_a():
    open_page("05 Add assignment")
    before = by_id(BRIEF_LABEL_ID)
    call("widget.text", id=BRIEF_LABEL_ID, text=BRIEF_LABEL_TEXT)
    after = by_id(BRIEF_LABEL_ID)
    print(f"A1 label: {before['text']!r} -> {after['text']!r}")

    field = by_id(BRIEF_FIELD_ID)
    call("widget.set", id=BRIEF_FIELD_ID, name="PlaceholderText", value=BRIEF_PLACEHOLDER)
    field2 = by_id(BRIEF_FIELD_ID)
    print(f"A2 placeholder: {field['placeholder']!r} -> {field2['placeholder']!r}")


def signup_spec():
    return {
        "event": "click",
        "cases": [
            {"name": "Enter your first name",
             "when": {"widget": SIGNUP_NAME, "equals": ""},
             "actions": [{"type": "setText", "target": SIGNUP_ERROR,
                          "text": "Enter your first name to continue."}]},
            {"name": "Enter an email",
             "when": {"widget": SIGNUP_EMAIL, "equals": ""},
             "actions": [{"type": "setText", "target": SIGNUP_ERROR,
                          "text": "Enter an email to continue."}]},
            {"name": "Enter a demo password",
             "when": {"widget": SIGNUP_PASSWORD, "equals": ""},
             "actions": [{"type": "setText", "target": SIGNUP_ERROR,
                          "text": "Enter a demo password to continue."}]},
            {"name": "Continue",
             "actions": [{"type": "storeGlobal", "variable": "TetherName", "widget": SIGNUP_NAME},
                         {"type": "navigate", "page": SIGNUP_TARGET}]},
        ],
    }


def task_b(avatar_text=None):
    open_page("02 Create account")
    before = call("interaction.get", id=SIGNUP_BUTTON)
    n_before = sum(len(e["cases"]) for e in before["events"])
    call("interaction.set", id=SIGNUP_BUTTON, spec=signup_spec(), replace=True)
    after = call("interaction.get", id=SIGNUP_BUTTON)
    n_after = sum(len(e["cases"]) for e in after["events"])
    acts = [a.get("type") for e in after["events"] for c in e["cases"] for a in c["actions"]]
    print(f"B1 app_signup cases {n_before} -> {n_after}; actions now {acts}")

    if avatar_text:
        open_page("04 Today")
        call("widget.text", id=AVATAR_INITIAL, text=avatar_text)
        w = by_id(AVATAR_INITIAL)
        print(f"B2 avatar initial text -> {w['text']!r}")


def save_export():
    res = call("project.save", path=str(WORK_RP))
    print("saved:", res)
    if EXPORT_DIR.exists():
        shutil.rmtree(EXPORT_DIR)
    EXPORT_DIR.mkdir(parents=True)
    out = call("export.html", output=str(EXPORT_DIR), timeout=300)
    print("exported:", out)


def verify():
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
    print("canvas check:", "ALL 17 AT 430px" if not bad else f"PROBLEMS {bad}")

    checks = {
        "05_add_assignment": ["Key requirements (one per line)",
                              "One requirement per line"],
        "02_create_account": ["TetherName"],
        "04_today": ["TetherName"],
    }
    for pg, needles in checks.items():
        blob = (files / pg / "data.js").read_text(encoding="utf-8", errors="replace")
        for n in needles:
            print(f"  {pg:22} contains {n!r}: {n in blob}")


def ensure_launch():
    """Reuse a running bridge; otherwise (re)open the working copy."""
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


def main():
    avatar = sys.argv[1] if len(sys.argv) > 1 else None
    ensure_launch()
    task_a()
    task_b(avatar)
    save_export()
    verify()


if __name__ == "__main__":
    main()
