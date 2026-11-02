"""Improvement 4: show the saved assignment brief (TetherBrief) on 07 Your plan.

Run on the Windows machine, inside an Axure session started by the native CLI
(see tools/axure-ai/README.md, "Chạy CLI trên máy này"):

    python Coursework/prototype/tether-final-build/improve-plan-brief.py

What it does:
1. Copies final-coursework.rp to final-coursework.before-brief.rp (only once).
2. Opens final-coursework.rp, goes to 07 Your plan.
3. Adds a paragraph "plan_brief" in the free space above the bottom nav.
4. Rebuilds the page OnLoad so it keeps the four existing actions and also
   shows TetherBrief in the new paragraph.
5. Saves, then exports HTML to final-preview-brief/ for checking.

Safe to run twice: an existing plan_brief widget is reused.
"""
import json
import shutil
import sys
from pathlib import Path

H = Path(__file__).resolve().parent
sys.path.insert(0, str(H / 'bridge-research/native-cli'))
import axure_cli as a  # noqa: E402

P = json.loads((H / 'app-page-ids.json').read_text())
RP = (H.parent / 'final-coursework.rp').resolve()
BACKUP = RP.with_name('final-coursework.before-brief.rp')
EXPORT = (H / 'final-preview-brief').resolve()


def c(op, **kw):
    r = a.request(dict(op=op, **kw))
    assert r.get('ok'), r
    return r['result']


def ws():
    return c('widget.list')


def named(n):
    return next(w['id'] for w in ws() if w['name'] == n)


def at(x, y, width):
    """Find a widget by its position (used for the unnamed description text)."""
    return next(w['id'] for w in ws()
                if w['bounds']['x'] == x and w['bounds']['y'] == y and w['bounds']['width'] == width)


if not BACKUP.exists():
    shutil.copy2(RP, BACKUP)
    print('Backup:', BACKUP)

c('project.open', path=str(RP))
c('page.open', id=P['plan'])

existing = [w for w in ws() if w['name'] == 'plan_brief']
if existing:
    brief = existing[0]['id']
else:
    brief = c('widget.create', kind='paragraph', name='plan_brief',
              text='Report and prototype for neurodiverse university learners.',
              x=28, y=782, width=374, height=48)['id']
print('plan_brief:', brief)

description = at(28, 225, 374)  # "HCI coursework · choose a step to work on."
actions = [{'type': 'showGlobal', 'variable': 'TetherAssignment', 'widget': description}]
actions += [{'type': 'showGlobalInput', 'variable': f'TetherStep{i}', 'widget': named(f'plan_step_{i}')}
            for i in range(1, 4)]
actions.append({'type': 'showGlobal', 'variable': 'TetherBrief', 'widget': brief})
print('OnLoad:', c('debug.page_load', replace=True, actions=actions))

c('page.open', id=P['welcome'])
print('Saved:', c('project.save'))

if EXPORT.exists() and any(EXPORT.iterdir()):
    print('Skip export: folder not empty ->', EXPORT)
else:
    c('project.new')
    c('project.open', path=str(RP))
    c('export.html', output=str(EXPORT))
    print('Exported:', EXPORT)
