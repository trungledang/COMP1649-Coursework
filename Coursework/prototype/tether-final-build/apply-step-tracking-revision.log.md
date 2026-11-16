# apply-step-tracking-revision.py — run log (2026-11-09)

Target file: `Coursework/prototype/tether-revision-2026-11-09.rp`
(via native bridge PID 23972, Axure RP 11.0.0.4150, hash dae5748f… verified by bridge)

## Attempt 1 (rehearsal — schema fix needed)
- backup created: `tether-revision-2026-11-09.before-step-tracking.rp` (353,963 bytes)
- globals added: TetherCurrent='0', TetherDone1..3=''
- `v2_start_1` widget created; `interaction.set` rejected top-level `cases`
  (needs `spec:{event,cases}`) → stopped with no partial state applied
  (new widget kept, interactions empty).

## Attempt 2 (final, idempotent re-run)
- backup: already exists → skipped
- globals: all 4 exist → skipped
- plan page (07 Your plan):
  - `v2_start_1` existed (from attempt 1, empty map) → interaction installed on it
  - `v2_start_2`, `v2_start_3` created @(250,472)/(250,588) 142x44 + interactions
    - case "Add an action": IF text of plan_step_i == "" →
      setText "Add a small action first." on the "Step i" title
    - case "Start current action": storeLiteral TetherCurrent=i,
      storeGlobal TetherStep{i} ← plan_step_i, storeGlobal TetherNext ← plan_step_i,
      navigate work (12f4c141…)
  - OnPageLoad rebuilt: show TetherAssignment→subtitle(5b08f0dd), inputs
    TetherStep1..3→plan_step_1..3, show TetherBrief→plan_brief (5 actions)
- work page (02 Continue your work):
  - `step_state` input created at (-200,-200) 80x16 (off-canvas tracker input)
  - `v2_done` overlay @(28,808) 374x54, 4 cases:
    IF step_state=="1|2|3" → storeLiteral TetherDone{i}="done" + navigate completed;
    final unconditional case replicates original navigate→completed
  - OnPageLoad rebuilt: showGlobalInput TetherCurrent→step_state,
    show TetherNext→action body (70d9659e) (2 actions)
- review page (06 Check requirements):
  - `v2_build_reset` overlay @(28,707) 374x54, 1 case, 13 actions:
    copyGlobal TetherDraftAssignment→TetherAssignment, copyGlobal TetherDraftBrief→TetherBrief,
    literals (TetherWhere/TetherNext/TetherStep1..3/TetherStudyTime as original),
    reset TetherDone1..3='' + TetherCurrent='0', navigate plan
- project.save: 363,983 bytes, dirty=false (same path)
- export.html → `export-step-tracking-2026-11-09/` (184 files)

## Verification
- `files/07_your_plan/data.js`: "Add a small action first.", "Start current action" ✔
- `files/02_continue_your_work/data.js`: OnPageLoad "Restore the saved thread",
  "Set text on step_state equal to value of TetherCurrent", cases Finish 1/2/3 ✔
- `files/06_check_requirements/data.js`: "Confirm, edit steps and reset tracking" ✔
- markers TetherCurrent/TetherDone1..3/v2_names/step_state present in all page data ✔

Note: first-run verify script read `data/document.js` (path does not exist in
RP 11 export; per-page data lives in `files/NN_name/data.js`). Script verify
corrected to `EXPORT.rglob('*.js')` for future runs.
