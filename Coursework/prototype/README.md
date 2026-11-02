# Task 5 Study Planner

Open `task5-edited.rp` in Axure RP 11. The project contains eight pages with editable native widgets, navigation links and global-variable actions. The original blank `task5.rp` in the course root was preserved; `backups/task5.original.rp` is a second original copy.

## Try the prototype

1. Start on **01 Assignment** and choose **Use example brief**. Review the requirements and choose **Build my plan**.
2. On **03 Your plan**, edit the task steps and choose **Choose study times**. Edit the day and time, choose **Save study time**, then use **Change study time** to review the saved values.
3. From **03 Your plan**, choose **This step feels difficult**, then **Break this into smaller steps**. Choose **Use this first action** to return to the plan with a smaller starting action.
4. From the saved schedule, choose **Mark first step complete** to view the example progress update.

## Scope and checks

- This is the first coursework progress prototype, not a finished app. Assignment interpretation and AI responses use a prepared example. Uploading arbitrary files, live AI generation and external calendar integration are not implemented.
- Six Axure global variables hold the task steps and chosen day/time during preview. They are intended to carry edits between linked pages; a fresh preview session starts from the example defaults.
- Progress completion uses a prepared confirmation page for the first step. It is not a complete task-management engine or persistent account storage.
- Automatic date validation and conflict detection are not implemented. The existing class time is displayed as context for the scheduling task.
- Verified by reloading with the installed Axure RP 11 native model: eight pages, 178 widgets, 48 navigation links with valid page targets, and saved expression actions. Native-rendered images of all eight pages were reviewed.
- The Axure desktop Preview click-through has not been tested in this environment. The student should run Preview and check the three main journeys before submission.

Historical builder: `../../tools/axure-native/` generated this prototype, but was retired and sent to Recycle Bin at the user's request on 2026-10-31. The prototype files remain intact. For new Axure work, read `../../tools/axure-ai/README.md`. That toolkit has verified Axvg layouts, native inputs and limited click interactions; reproducing this prototype's global-variable flows has not yet been verified with it.
