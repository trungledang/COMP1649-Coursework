# StudyFlow web prototype — 19 October 2026

File: `studyflow-web-practice-v2.rp` (Axure RP 11).

This is an AI-assisted development/practice version, not a verified submission-ready final. The brief limits generative AI to preparation and prohibits submitting AI-generated work as your own. Review the brief and develop your own assessed design and rationale.

## Included

- 22 editable native Axure pages, including login demo, Today, courses, assignment overview, Materials, requirements, Plan, schedule, Help and account.
- Native dynamic panels: document previews, source-selection toggles, contextual support with three distinct reasons, smaller-action acceptance/completion/undo, source explanation, connection details.
- Editable requirements, four plan steps and session day/time. Save buttons contain native global-variable assignment actions, and destination pages restore values on load.
- Original `task5.rp` and earlier `task5-edited.rp` preserved.

## Verification performed

The file was reopened using the installed Axure native model. All page navigation destinations and dynamic-panel state targets were checked, including nested widgets. Pages and individual panel states were rendered for visual inspection.

This is structural/render verification, NOT a browser or Axure Preview click-through. No claim is made that all runtime behavior has passed an end-to-end test.

## Still incomplete against the requested final

- Visual design follows the approved mockups but does not exactly reproduce their icons, typography or finer details.
- Calendar placement is illustrative, not calculated from edited values. There is no time validation, conflict detection, drag-and-drop or day/week switching.
- Source selection and document preview are local panel states. They do not drive real AI output and are not persisted across page navigation.
- Upload, AI replies, Google authentication and Calendar integration are prepared simulations. No account credentials are requested.
- Overall task completion is a prepared progress screen, not a persistent multi-task progress engine. Smaller-action completion/undo is a real local panel-state interaction.
- File search, rename and delete-with-confirmation are not implemented.
- A smaller-action panel resets if the page is revisited. Plan edits and study-time values use global variables during Preview, not durable storage.

## Preview checks to perform

1. Start at `01 login` and continue as Alex. Open the assignment, Materials and Plan.
2. In Materials, preview each filename and toggle each source checkbox. Distinguish preview selection from AI source selection.
3. In Plan, open/close Why this step; inspect the source page.
4. Open I'm stuck. Exercise all three reasons. Accept a smaller action, mark only that action done, then undo. Confirm the parent task remains unchanged.
5. Edit plan wording and save; navigate away and back. Change the session day/time and save; check Today and Schedule.
6. Check Cancel, Back, account and sign-out paths. Do not treat Google buttons as real authentication.

The requested submission-ready state has not been reached. These remaining gaps must not be hidden by renaming this file “final”.
