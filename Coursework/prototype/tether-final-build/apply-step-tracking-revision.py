"""Apply step-tracking patch (Improvement guide, item 5) to tether-revision-2026-11-09.rp.

Requires: Axure bridge (bridge-research/native-cli) already running with the
revision project open. Steps:

1.  Backup the .rp next to the original (only if missing).
2.  Add globals TetherCurrent='0', TetherDone1..3='' (idempotent).
3.  Plan page:
      - overlay v2_start_1..3 on personalized_start_1..3, replicating the old
        cases and adding TetherCurrent/TetherStep_i/TetherNext stores.
      - rebuild OnPageLoad (show assignment, brief, step texts).
4.  Work page:
      - hidden input step_state (off-canvas) + OnPageLoad storing TetherCurrent
        in it, and showing TetherNext on the action body text.
      - overlay v2_done on v3_finish_step: IF step_state = 1/2/3 then mark
        TetherDone_i='done', else replicate the original navigate.
5.  Review page:
      - overlay v2_build_reset on app_build: replicate the original commit
        actions (copyGlobal TetherDraft->Tether, literals, navigate plan) and
        reset TetherDone1..3 + TetherCurrent.
6.  project.save (same path), export.html into a fresh empty folder, verify
    data/document.js mentions the new variables/widgets.
"""
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

H = Path(__file__).resolve().parent
sys.path.insert(0, str(H / 'bridge-research/native-cli'))
import axure_cli as a

P = json.loads((H / 'app-page-ids.json').read_text(encoding='utf-8'))
RP = (H.parent / 'tether-revision-2026-11-09.rp').resolve()
BACKUP = RP.with_name('tether-revision-2026-11-09.before-step-tracking.rp')
EXPORT = H / ('export-step-tracking-' + datetime.now().strftime('%Y-%m-%d'))

LOG = []
def log(msg):
    print(msg)
    LOG.append(msg)

def c(op, **kw):
    r = a.request(dict(op=op, **kw))
    if not r.get('ok'):
        raise RuntimeError(f'{op} FAILED: {r}')
    return r['result']

def open_page(key):
    c('page.open', id=P[key])

def ws():
    return c('widget.list')

def wid_by_name(name):
    for w in ws():
        if w['name'] == name:
            return w['id']
    return None

def require_wid(name):
    i = wid_by_name(name)
    if i is None:
        raise RuntimeError(f'widget not found on current page: {name}')
    return i

def ensure_backup():
    if BACKUP.exists():
        log(f'backup exists: {BACKUP.name}')
    else:
        st = c('status')
        proj = st['project']
        if proj.get('dirty'):
            raise RuntimeError('project dirty; save or inspect before backup')
        shutil.copy2(RP, BACKUP)
        log(f'backup created: {BACKUP.name} ({BACKUP.stat().st_size} bytes)')

def add_globals():
    known = {v['name'] for v in c('debug.vars')['variables']}
    for name, val in [('TetherCurrent', '0'), ('TetherDone1', ''),
                      ('TetherDone2', ''), ('TetherDone3', '')]:
        if name in known:
            log(f'  var exists: {name}')
        else:
            c('debug.var_add', name=name, value=val)
            log(f'  var added: {name}={val!r}')

def overlay(name, x, y, w, h, cases):
    i = wid_by_name(name)
    if i is None:
        i = c('widget.create', kind='paragraph', name=name, text='',
              x=x, y=y, width=w, height=h)['id']
        log(f'  widget created: {name} @({x},{y}) {w}x{h}')
    events = c('interaction.get', id=i)['events']
    if events:
        if len(events) > 1 or events[0].get('type') != 'OnClick':
            raise RuntimeError(f'{name}: unexpected existing interactions, inspect first')
        log(f'  overlay already installed, skip: {name}')
        return
    c('interaction.set', id=i, spec={'event': 'click', 'cases': cases})
    log(f'  interaction installed: {name} ({len(cases)} cases)')

def page_load_build(key, actions):
    open_page(key)
    events = c('debug.diagram').get('events') or []
    if events:
        raise RuntimeError(f'{key}: page interactions already exist, inspect '
                           f'before replacing (op debug.page_load replace=true)')
    c('debug.page_load', actions=actions)
    log(f'  {key}: OnPageLoad built with {len(actions)} actions')

# ------------------------------------------------------------------
# 1. Backup
# ------------------------------------------------------------------
log('--- backup ---')
ensure_backup()

# ------------------------------------------------------------------
# 2. Globals
# ------------------------------------------------------------------
log('--- globals ---')
add_globals()

# ------------------------------------------------------------------
# 3. Plan page
# ------------------------------------------------------------------
log('--- plan page ---')
open_page('plan')

step_in = {i: require_wid(f'plan_step_{i}') for i in (1, 2, 3)}
start_i = {i: require_wid(f'personalized_start_{i}') for i in (1, 2, 3)}
title_i = {1: 'dcd11af4-7ba9-4c6b-98a8-7f086ab4134a',   # "Step 1"
           2: '13fa3eb4-78e3-4269-ac3e-500363862679',   # "Step 2"
           3: '30d1a4a4-4a29-4767-a376-513bf8efa962'}   # "Step 3"

class PlanWidgetResolver:
    def __getitem__(self, wid):
        for w in ws():
            if w['id'].startswith(wid[:8]):
                return w['id']
        raise RuntimeError('widget not on plan page: ' + wid)
PLAN_W = PlanWidgetResolver()
title_i = {i: PLAN_W[v] for i, v in title_i.items()}

for i in (1, 2, 3):
    b = next(w['bounds'] for w in ws() if w['name'] == f'personalized_start_{i}')
    overlay(f'v2_start_{i}', b['x'], b['y'], b['width'], b['height'], cases=[
        {'name': 'Add an action',
         'when': {'widget': step_in[i], 'equals': ''},
         'actions': [{'type': 'setText', 'target': title_i[i],
                      'text': 'Add a small action first.'}]},
        {'name': 'Start current action',
         'actions': [{'type': 'storeLiteral', 'variable': 'TetherCurrent',
                      'value': str(i)},
                     {'type': 'storeGlobal', 'variable': f'TetherStep{i}',
                      'widget': step_in[i]},
                     {'type': 'storeGlobal', 'variable': 'TetherNext',
                      'widget': step_in[i]},
                     {'type': 'navigate', 'page': P['work']}]},
    ])

page_load_build('plan', [
    {'type': 'showGlobal', 'variable': 'TetherAssignment',
     'widget': PLAN_W['5b08f0dd']},                # subtitle under "Your plan"
    {'type': 'showGlobalInput', 'variable': 'TetherStep1', 'widget': step_in[1]},
    {'type': 'showGlobalInput', 'variable': 'TetherStep2', 'widget': step_in[2]},
    {'type': 'showGlobalInput', 'variable': 'TetherStep3', 'widget': step_in[3]},
    {'type': 'showGlobal', 'variable': 'TetherBrief', 'widget': require_wid('plan_brief')},
])

# ------------------------------------------------------------------
# 4. Work page
# ------------------------------------------------------------------
log('--- work page ---')
open_page('work')

state_id = wid_by_name('step_state')
if state_id:
    log('  step_state exists, skip creation')
else:
    state_id = c('widget.create', kind='input', name='step_state', text='',
                 x=-200, y=-200, width=80, height=16)['id']
    log('  step_state created (hidden off-canvas input)')

finish_b = next(w['bounds'] for w in ws() if w['name'] == 'v3_finish_step')
action_body = None
for w in ws():
    bnd = w['bounds']
    if not w.get('name') and bnd['x'] == 88 and bnd['y'] == 373:
        action_body = w['id']                       # "Add one example..." body
if action_body is None:
    raise RuntimeError('work action body widget not found')

overlay('v2_done', finish_b['x'], finish_b['y'], finish_b['width'],
        finish_b['height'], cases=[
    {'name': 'Finish step 1',
     'when': {'widget': state_id, 'equals': '1'},
     'actions': [{'type': 'storeLiteral', 'variable': 'TetherDone1', 'value': 'done'},
                 {'type': 'navigate', 'page': P['completed']}]},
    {'name': 'Finish step 2',
     'when': {'widget': state_id, 'equals': '2'},
     'actions': [{'type': 'storeLiteral', 'variable': 'TetherDone2', 'value': 'done'},
                 {'type': 'navigate', 'page': P['completed']}]},
    {'name': 'Finish step 3',
     'when': {'widget': state_id, 'equals': '3'},
     'actions': [{'type': 'storeLiteral', 'variable': 'TetherDone3', 'value': 'done'},
                 {'type': 'navigate', 'page': P['completed']}]},
    {'name': 'Continue',                             # replicate original
     'actions': [{'type': 'navigate', 'page': P['completed']}]},
])

page_load_build('work', [
    {'type': 'showGlobalInput', 'variable': 'TetherCurrent', 'widget': state_id},
    {'type': 'showGlobal', 'variable': 'TetherNext', 'widget': action_body},
])

# ------------------------------------------------------------------
# 5. Review page
# ------------------------------------------------------------------
log('--- review page ---')
open_page('review')
build_b = next(w['bounds'] for w in ws() if w['name'] == 'app_build')
overlay('v2_build_reset', build_b['x'], build_b['y'], build_b['width'],
        build_b['height'], cases=[
    {'name': 'Confirm, edit steps and reset tracking',
     'actions': [
        {'type': 'copyGlobal', 'variable': 'TetherAssignment',
         'source': 'TetherDraftAssignment'},
        {'type': 'copyGlobal', 'variable': 'TetherBrief', 'source': 'TetherDraftBrief'},
        {'type': 'storeLiteral', 'variable': 'TetherWhere',
         'value': 'Ready to start this assignment.'},
        {'type': 'storeLiteral', 'variable': 'TetherNext',
         'value': 'Identify the main requirements.'},
        {'type': 'storeLiteral', 'variable': 'TetherStep1',
         'value': 'Identify the main requirements.'},
        {'type': 'storeLiteral', 'variable': 'TetherStep2',
         'value': 'Find two useful sources.'},
        {'type': 'storeLiteral', 'variable': 'TetherStep3',
         'value': 'Draft one paragraph.'},
        {'type': 'storeLiteral', 'variable': 'TetherStudyTime',
         'value': 'Tomorrow, 09:00 - 10 minutes'},
        {'type': 'storeLiteral', 'variable': 'TetherDone1', 'value': ''},
        {'type': 'storeLiteral', 'variable': 'TetherDone2', 'value': ''},
        {'type': 'storeLiteral', 'variable': 'TetherDone3', 'value': ''},
        {'type': 'storeLiteral', 'variable': 'TetherCurrent', 'value': '0'},
        {'type': 'navigate', 'page': P['plan']},
     ]},
])

# ------------------------------------------------------------------
# 6. Save + export
# ------------------------------------------------------------------
log('--- save ---')
saved = c('project.save')
log(f'saved: {saved}')

log('--- export ---')
EXPORT.parent.mkdir(parents=True, exist_ok=True)
if EXPORT.exists() and any(EXPORT.iterdir()):
    raise RuntimeError(f'export destination not empty: {EXPORT}')
r = c('export.html', output=str(EXPORT))
log(f'exported: {EXPORT} ({r["files"]} files)')

docjs_text = ''.join(
    p.read_text(encoding='utf-8', errors='ignore') for p in EXPORT.rglob('*.js'))
must = ['TetherCurrent', 'TetherDone1', 'v2_start_1', 'v2_done', 'v2_build_reset',
        'step_state', 'TetherStep1']
found = {m: (m in docjs_text) for m in must}
log(f'verify export ({EXPORT.name}): {found}')
missing = [k for k, v in found.items() if not v]
if missing:
    raise RuntimeError(f'markers missing in export: {missing}')

(Path(__file__).with_suffix('.log')).write_text(
    '\n'.join(LOG) + f'\n\nstatus: {json.dumps(c("status")["project"], indent=1)}\n',
    encoding='utf-8')
log('--- step tracking patch complete ---')
