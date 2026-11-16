"""Automated improvements for Tether ADHD Companion prototype.

Launches Axure with bridge, opens Tether_ADHD_Companion_Final.rp, and:
1. Adds TetherCurrent, TetherDone1/2/3 global variables
2. Creates overlay hotspots on 07 Your plan to track current step number
3. Creates overlay on 06 Check requirements to reset done flags on new assignment
4. Rebuilds OnPageLoad on plan page with all needed actions
5. Saves and exports HTML for preview/screenshots
"""
import json
import shutil
import sys
import time
from pathlib import Path

H = Path(__file__).resolve().parent
sys.path.insert(0, str(H / 'bridge-research/native-cli'))
import axure_cli as a

P = json.loads((H / 'app-page-ids.json').read_text())
RP = (H.parent / 'Tether_ADHD_Companion_Final.rp').resolve()
BACKUP = RP.with_name('Tether_ADHD_Companion_Final.before-step-tracking.rp')
EXPORT = (H / 'final-export-step-tracking').resolve()


def c(op, **kw):
    r = a.request(dict(op=op, **kw))
    assert r.get('ok'), f'FAILED {op}: {r}'
    return r['result']


def open_page(k):
    c('page.open', id=P[k])


def ws():
    return c('widget.list')


def named(n):
    return next(w['id'] for w in ws() if w['name'] == n)


def find_named(n):
    return next((w for w in ws() if w['name'] == n), None)


def show(v, wid):
    return {'type': 'showGlobal', 'variable': v, 'widget': wid}


def show_input(v, wid):
    return {'type': 'showGlobalInput', 'variable': v, 'widget': wid}


def store_literal(v, val):
    return {'type': 'storeLiteral', 'variable': v, 'value': val}


def store_global(v, wid):
    return {'type': 'storeGlobal', 'variable': v, 'widget': wid}


def navigate(page_key):
    return {'type': 'navigate', 'page': P[page_key]}


def hotspot(name, x, y, w, h, actions):
    existing = find_named(name)
    if existing:
        print(f'  {name} already exists, skipping')
        return existing['id']
    wid = c('widget.create', kind='paragraph', name=name, text='',
            x=x, y=y, width=w, height=h)['id']
    c('interaction.set', id=wid, spec={
        'event': 'click',
        'cases': [{'name': name, 'actions': actions}]
    })
    print(f'  Created: {name}')
    return wid


# ============================================================
# 0. Backup
# ============================================================
if not BACKUP.exists():
    shutil.copy2(RP, BACKUP)
    print(f'Backup -> {BACKUP.name}')
else:
    print(f'Backup exists: {BACKUP.name}')

# ============================================================
# 1. Launch Axure with bridge
# ============================================================
print('\n--- Launching Axure with bridge ---')
launch_result = a.launch(project=str(RP), app='C:/Program Files (x86)/Axure/Axure RP 11/AxureRP11.exe')
print(f'Launch result: ok={launch_result.get("ok")}')
if not launch_result.get('ok'):
    print(f'Launch detail: {launch_result}')
    sys.exit(1)

time.sleep(2)
print(f'Status: {c("status")}')

# ============================================================
# 2. Add global variables
# ============================================================
print('\n--- Adding global variables ---')
open_page('plan')
known = {v['name'] for v in c('debug.vars')['variables']}
print(f'Existing variables ({len(known)}): {sorted(known)}')

new_vars = [
    ('TetherCurrent', '0'),
    ('TetherDone1', ''),
    ('TetherDone2', ''),
    ('TetherDone3', ''),
]
for v, default in new_vars:
    if v not in known:
        c('debug.var_add', name=v, value=default)
        print(f'  Added: {v} = {repr(default)}')
    else:
        print(f'  Already exists: {v}')

# ============================================================
# 3. Plan page: overlay hotspots that set TetherCurrent
# ============================================================
print('\n--- Plan page: step tracking overlays ---')
widgets_list = ws()

# Find plan_step input widgets
step_inputs = {}
for i in range(1, 4):
    w = find_named(f'plan_step_{i}')
    if w:
        step_inputs[i] = w['id']
        print(f'  Found plan_step_{i}: {w["id"][:8]}...')
    else:
        print(f'  WARNING: plan_step_{i} not found!')

# Create overlay hotspots for "Start this step" (sit on top of personalized_start_X)
# Original positions from personalize-app.py: x=250, y=Y+58, w=142, h=26
# where Y = 313, 415, 517 for steps 1, 2, 3
for i, base_y in enumerate([313, 415, 517], 1):
    if i not in step_inputs:
        print(f'  Skipping v2_start_{i}: input not found')
        continue
    actions = [
        store_global(f'TetherStep{i}', step_inputs[i]),
        store_global('TetherNext', step_inputs[i]),
        store_literal('TetherCurrent', str(i)),
        navigate('work'),
    ]
    hotspot(f'v2_start_{i}', 250, base_y + 58, 142, 26, actions)

# ============================================================
# 4. Plan page: rebuild OnPageLoad
# ============================================================
print('\n--- Plan page: update OnPageLoad ---')
# Find the description text widget (shows assignment name)
desc_widget = None
for w in ws():
    b = w.get('bounds', {})
    if b.get('x') == 28 and b.get('y') == 225 and b.get('width') == 374:
        desc_widget = w['id']
        break

load_actions = []
if desc_widget:
    load_actions.append(show('TetherAssignment', desc_widget))
    print(f'  Assignment display: {desc_widget[:8]}...')

for i in range(1, 4):
    if i in step_inputs:
        load_actions.append(show_input(f'TetherStep{i}', step_inputs[i]))

# Include plan_brief if it exists
brief_w = find_named('plan_brief')
if brief_w:
    load_actions.append(show('TetherBrief', brief_w['id']))
    print(f'  Plan brief: {brief_w["id"][:8]}...')

if load_actions:
    c('debug.page_load', replace=True, actions=load_actions)
    print(f'  OnPageLoad set with {len(load_actions)} actions')

# ============================================================
# 5. Review page: reset overlay for "Build plan" button
# ============================================================
print('\n--- Review page: reset overlay ---')
open_page('review')

build_btn = find_named('app_build')
if build_btn:
    bx = build_btn['bounds']['x']
    by = build_btn['bounds']['y']
    bw = build_btn['bounds']['width']
    bh = build_btn['bounds']['height']
    print(f'  Found app_build at ({bx},{by}) {bw}x{bh}')
else:
    # Fallback from wire-app.py
    bx, by, bw, bh = 28, 707, 374, 54
    print(f'  app_build not found, using fallback position')

reset_actions = [
    store_literal('TetherDone1', ''),
    store_literal('TetherDone2', ''),
    store_literal('TetherDone3', ''),
    store_literal('TetherCurrent', '0'),
    navigate('plan'),
]
hotspot('v2_build_reset', bx, by, bw, bh, reset_actions)

# ============================================================
# 6. Save
# ============================================================
print('\n--- Saving ---')
open_page('welcome')
save_result = c('project.save')
print(f'Saved: {save_result}')

# ============================================================
# 7. Export HTML
# ============================================================
print('\n--- Exporting HTML ---')
EXPORT.mkdir(parents=True, exist_ok=True)
if any(EXPORT.iterdir()):
    print(f'Export folder not empty, skipping: {EXPORT}')
else:
    c('project.new')
    c('project.open', path=str(RP))
    c('export.html', output=str(EXPORT))
    print(f'Exported to: {EXPORT}')

print('\n=== Step tracking improvements complete! ===')
print(f'File: {RP}')
print(f'Backup: {BACKUP}')
