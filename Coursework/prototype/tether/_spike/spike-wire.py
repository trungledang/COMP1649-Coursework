"""Spike 01 — wire native behaviour onto the pasted Axvg page and verify."""
import sys, json, os
from pathlib import Path

KIT = Path(r"E:\Hoc tap\Mon hoc\Năm 3 kì 1\COMP1649_HCI\tools\axure-ai")
sys.path.insert(0, str(KIT / "native-cli"))
os.environ["REVERSE_CLI_CACHE_DIR"] = "E:/ai-cache/axure-pilot/cache"
import axure_cli as ax

OUT = Path(r"E:\Hoc tap\Mon hoc\Năm 3 kì 1\COMP1649_HCI\Coursework\prototype\tether\_spike")
LOG = OUT / "wire-log.jsonl"


def call(op, **kw):
    payload = dict(op=op, **kw)
    r = ax.request(payload)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"op": op, "payload": payload, "response": r}, ensure_ascii=False) + "\n")
    if not r.get("ok"):
        raise RuntimeError(f"{op} failed: {r}")
    return r["result"]


def find(name):
    for w in call("widget.list"):
        if w["name"] == name:
            return w
    raise KeyError(name)


def main():
    # --- offset from the pasted frame (Axure does not always paste at 0,0)
    bg = find("Spike 01 BG")
    dx, dy = bg["bounds"]["x"], bg["bounds"]["y"]
    print("paste offset:", dx, dy)

    p1 = call("page.list")["activeId"]
    p2 = call("page.create", name="S2 target")["page"]["Id"]

    # --- native input inside the designed field
    q1 = find("q1_field")["bounds"]
    input1 = call(
        "widget.create", kind="input", name="q1_input", text="",
        placeholder="e.g. mid-sentence",
        x=q1["x"], y=q1["y"], width=q1["width"], height=q1["height"],
    )["id"]

    q2 = find("q2_field")["bounds"]
    input2 = call(
        "widget.create", kind="input", name="q2_input", text="",
        placeholder="e.g. paste the source link",
        x=q2["x"], y=q2["y"], width=q2["width"], height=q2["height"],
    )["id"]

    # --- invisible hotspot over the designed primary button
    btn = find("primary_bg")["bounds"]
    hotspot = call(
        "widget.create", kind="paragraph", name="hotspot_primary", text="",
        x=btn["x"], y=btn["y"], width=btn["width"], height=btn["height"],
    )["id"]

    footer = find("footer")["id"]
    chip_a, chip_a_label = find("chip_a")["id"], find("chip_a_label")["id"]
    chip_b, chip_b_label = find("chip_b")["id"], find("chip_b_label")["id"]
    move_text = find("move_text")["id"]
    primary_label = find("primary_label")["id"]

    # --- chips fill the fields (real state, visible, no hidden variables needed)
    call("interaction.set", id=chip_a, spec={"event": "click", "cases": [{
        "name": "chip a", "actions": [
            {"type": "setText", "target": input1, "text": "Mid-sentence"},
            {"type": "setText", "target": footer, "text": "Got it. One more."},
        ]}]})
    call("interaction.set", id=chip_a_label, spec={"event": "click", "cases": [{
        "name": "chip a label", "actions": [
            {"type": "setText", "target": input1, "text": "Mid-sentence"},
            {"type": "setText", "target": footer, "text": "Got it. One more."},
        ]}]})

    call("interaction.set", id=chip_b, spec={"event": "click", "cases": [{
        "name": "chip b", "actions": [
            {"type": "setText", "target": input2, "text": "Paste the source link"},
            {"type": "setText", "target": footer, "text": "Got it. One more."},
        ]}]})
    call("interaction.set", id=chip_b_label, spec={"event": "click", "cases": [{
        "name": "chip b label", "actions": [
            {"type": "setText", "target": input2, "text": "Paste the source link"},
            {"type": "setText", "target": footer, "text": "Got it. One more."},
        ]}]})

    # --- primary: all-empty -> both empty -> each empty -> navigate
    call("interaction.set", id=hotspot, spec={"event": "click", "cases": [
        {"name": "nothing chosen",
         "when": {"all": [{"widget": input1, "equals": ""}, {"widget": input2, "equals": ""}]},
         "actions": [{"type": "setText", "target": footer, "text": "Two answers first — where you stopped, and the next move."}]},
        {"name": "no q1",
         "when": {"widget": input1, "equals": ""},
         "actions": [{"type": "setText", "target": footer, "text": "Where did you stop? Pick a chip or type it."}]},
        {"name": "no q2",
         "when": {"widget": input2, "equals": ""},
         "actions": [{"type": "setText", "target": footer, "text": "What is the next physical move?"}]},
        {"name": "ok",
         "actions": [
             {"type": "setText", "target": primary_label, "text": "Tied off ✓"},
             {"type": "setText", "target": move_text, "text": "Thread saved. Next time you open Tether, this is the first thing you see."},
             {"type": "navigate", "page": p2},
         ]},
    ]})

    # --- prove styled text survives setText: restyle check via a separate click
    call("interaction.set", id=move_text, spec={"event": "click", "cases": [{
        "name": "restyle", "actions": [
            {"type": "setText", "target": move_text,
             "text": "Short."}]}]})

    print("page1", p1, "page2", p2)
    print("input1", input1, "input2", input2, "hotspot", hotspot)

    call("project.save", path=str(OUT / "spike.rp"))
    call("export.html", output=str(OUT / "html"))
    print("saved + exported")


if __name__ == "__main__":
    main()
