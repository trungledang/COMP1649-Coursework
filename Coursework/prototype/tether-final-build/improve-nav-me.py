"""Rename the bottom-nav label "Settings" to "Me" and clear the top-right
"Today" label on 04 Today (that corner is where the avatar goes).

Run on the Windows machine, inside an Axure session started by the native CLI
(see tools/axure-ai/README.md):

    python Coursework/prototype/tether-final-build/improve-nav-me.py

- Backs up final-coursework.rp to final-coursework.before-me.rp (only once).
- Only changes text; links and interactions stay the same.
- Safe to run twice: it skips labels that already say "Me".
The avatar circle itself is drawn by hand (HUONG-DAN-CAI-THIEN.md, mục 7).
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
BACKUP = RP.with_name('final-coursework.before-me.rp')
NAV_PAGES = ['dashboard', 'plan', 'scheduled', 'settings']  # pages with the bottom nav


def c(op, **kw):
    r = a.request(dict(op=op, **kw))
    assert r.get('ok'), r
    return r['result']


if not BACKUP.exists():
    shutil.copy2(RP, BACKUP)
    print('Backup:', BACKUP)

c('project.open', path=str(RP))

for key in NAV_PAGES:
    c('page.open', id=P[key])
    labels = [w for w in c('widget.list')
              if w.get('text') == 'Settings' and w['bounds']['y'] >= 830]
    for w in labels:
        c('widget.text', id=w['id'], text='Me')
    print(f'{key}: renamed {len(labels)} nav label(s)')

c('page.open', id=P['dashboard'])
corner = [w for w in c('widget.list')
          if w.get('text') == 'Today' and w['bounds']['y'] < 120]
for w in corner:
    c('widget.text', id=w['id'], text='')
print(f'dashboard: cleared {len(corner)} top-right label(s)')

c('page.open', id=P['welcome'])
print('Saved:', c('project.save'))
