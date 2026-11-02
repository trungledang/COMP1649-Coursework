"""Spike 01 — drive the exported HTML and prove the interaction stack works."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

SPIKE = Path(r"E:\Hoc tap\Mon hoc\Năm 3 kì 1\COMP1649_HCI\Coursework\prototype\tether\_spike")
HTML = (SPIKE / "html" / "page_1.html").as_uri()
SHOTS = SPIKE / "shots"
SHOTS.mkdir(exist_ok=True)

report = {}


def label_text(page, name):
    el = page.locator(f'[data-label="{name}"] .text')
    return el.inner_text().strip()


def box(page, name):
    return page.locator(f'[data-label="{name}"]').first.bounding_box()


def click(page, name):
    b = box(page, name)
    page.mouse.click(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
    page.wait_for_timeout(250)


with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge")
    page = b.new_page(viewport={"width": 760, "height": 900}, device_scale_factor=2)
    page.goto(HTML)
    page.wait_for_timeout(1200)
    page.screenshot(path=str(SHOTS / "01-initial.png"), full_page=True)

    report["footer_initial"] = label_text(page, "footer")
    report["move_text_initial"] = label_text(page, "move_text")

    # 1. styled text survives setText
    click(page, "move_text")
    report["move_text_after_click"] = label_text(page, "move_text")
    report["move_text_style"] = page.eval_on_selector(
        '[data-label="move_text"] .text span',
        "el => { const s = getComputedStyle(el); return {font: s.fontFamily, size: s.fontSize, weight: s.fontWeight, color: s.color}; }",
    )
    page.screenshot(path=str(SHOTS / "02-restyled.png"), full_page=True)

    # 2. empty-state error from the invisible hotspot
    click(page, "hotspot_primary")
    report["error_all_empty"] = label_text(page, "footer")
    page.screenshot(path=str(SHOTS / "03-error-both-empty.png"), full_page=True)

    # 3. chip fills the input, then partial error
    click(page, "chip_a_label")
    report["q1_after_chip"] = page.input_value('[data-label="q1_input"] input')
    click(page, "hotspot_primary")
    report["error_missing_q2"] = label_text(page, "footer")
    page.screenshot(path=str(SHOTS / "04-error-missing-q2.png"), full_page=True)

    # 4. second chip + success path
    click(page, "chip_b_label")
    report["q2_after_chip"] = page.input_value('[data-label="q2_input"] input')
    page.screenshot(path=str(SHOTS / "05-both-filled.png"), full_page=True)

    click(page, "hotspot_primary")
    page.wait_for_timeout(900)
    report["url_after_ok"] = page.url.split("/")[-1]
    page.screenshot(path=str(SHOTS / "06-navigated.png"), full_page=True)

    # 5. is the empty hotspot actually invisible?
    page.goto(HTML)
    page.wait_for_timeout(900)
    report["hotspot_visible"] = page.eval_on_selector(
        '[data-label="hotspot_primary"]',
        "el => { const s = getComputedStyle(el); return {bg: s.backgroundColor, border: s.borderTopWidth, opacity: s.opacity, text: el.innerText.trim()}; }",
    )
    b.close()

print(json.dumps(report, indent=2, ensure_ascii=False))
(SPIKE / "spike-report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
