"""Inspect the pages and widgets needed for tasks A-C (Tether prototype)."""
import json
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent / "bridge-research" / "native-cli"
sys.path.insert(0, str(KIT))
import axure_cli as a  # noqa: E402


def call(op, **kw):
    out = a.request(dict(op=op, **kw), 60)
    if not out.get("ok"):
        raise RuntimeError(out.get("error"))
    return out.get("result")


def pages():
    flat = []

    def walk(ns):
        for n in ns or []:
            flat.append(n)
            walk(n.get("Children"))

    walk(call("page.list").get("pages"))
    return flat


def pid(n):
    for p in pages():
        if p.get("Name") == n:
            return p["Id"]
    raise KeyError(n)


def summarize(w):
    ix = call("interaction.get", id=w["id"])
    acts = []
    for e in ix.get("events") or []:
        for c in e.get("cases") or []:
            for act in c.get("actions") or []:
                if act.get("type") == "navigate":
                    acts.append("nav->" + str(act.get("page"))[:8])
                elif act.get("type") == "expression":
                    d = act.get("description") or ""
                    acts.append("expr:" + d[:60])
                else:
                    acts.append(act.get("type"))
    b = w["bounds"]
    return {
        "name": w["name"],
        "type": w["type"].split(".")[-1],
        "id": w["id"],
        "x": b["x"], "y": b["y"], "w": b["width"], "h": b["height"],
        "text": w.get("text"),
        "placeholder": w.get("placeholder"),
        "acts": acts,
    }


def main():
    out = {}
    for pg in ["02 Create account", "04 Today", "01 My study desk", "10 Your space",
               "08 Study time", "05 Add assignment", "07 Your plan"]:
        call("page.open", id=pid(pg))
        ws = [summarize(w) for w in call("widget.list")]
        out[pg] = ws
    # full interaction map of app_signup (for a faithful rebuild)
    call("page.open", id=pid("02 Create account"))
    for w in call("widget.list"):
        if w["name"] == "app_signup":
            out["app_signup_map"] = call("interaction.get", id=w["id"])
    # page-level OnLoad maps
    for pg in ["04 Today", "10 Your space"]:
        call("page.open", id=pid(pg))
        out[f"diagram::{pg}"] = call("debug.diagram")
    Path(__file__).with_name("inspect-tasks.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("written inspect-tasks.json")


if __name__ == "__main__":
    main()
