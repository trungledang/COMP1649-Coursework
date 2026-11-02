# Task 5 — Research questions for review

## Status and scope

Topic A has been selected by the student. The student selected options Q2, Q3 and Q4 from `research-question-options.md`, with a focus on a simple, understandable interface. The following wording is an AI-assisted planning draft for the student to review and adapt, not a final assessed submission.

The intended product supports university students with ADHD in managing coursework. The proposed journey is: provide an assignment document, review the interpreted requirements, answer clarification questions, edit proposed task steps, adjust a suggested schedule, and request help when a step feels difficult.

The Axure prototype will simulate AI responses for prepared scenarios. The questions concern interaction with the prototype, not the performance of a live AI model or long-term academic outcomes.

## Working product concept — planning notes

**Topic:** A — A digital application for neurodiverse learners in higher education.

**Target group:** University students with ADHD who want support in planning and managing coursework.

**Proposed concept:** An AI-assisted coursework planner. Students provide an assignment document and review the requirements interpreted by the assistant. The assistant asks for missing information, such as the deadline, existing progress and available study times. It then proposes manageable task steps and a schedule that students can edit and confirm.

During task execution, students can mark steps as completed or request help when they are unsure how to proceed. The support flow offers clarification or a smaller task breakdown, which students can review before updating their plan.

**Core prototype journeys:**

1. Review an assignment and its proposed task breakdown, then identify a concrete first action.
2. Review and adjust a proposed study schedule to fit available time.
3. Request support for a difficult step and identify a next action.

**UX priorities:** Clear navigation, visible next actions, editable suggestions, understandable feedback and user control. Icons will have text labels. Illustrations may be used where they support understanding; their benefit remains a design assumption to evaluate.

**Implementation scope:** A new Axure RP prototype using prepared assignment scenarios and simulated AI responses. The existing PhoneShop Task 3 file is a separate exercise, not the coursework prototype. No live AI service or external calendar integration has been implemented.

## Three candidate research questions

### RQ1 — Identifying a starting action

**How easily can university students with ADHD identify a concrete first action when reviewing an editable, AI-proposed breakdown of a coursework assignment?**

Focus: whether students understand what concrete action to take first after reviewing the proposed steps.

- Prototype interaction: review the assignment summary, inspect and edit the proposed steps, and select a first action.
- Example test activity: using a prepared assignment scenario, select the step to start with and explain what you would do first.
- Possible evidence: whether the selected action is relevant to the scenario and prerequisites, time to select it, requests for moderator help, and a rating of clarity. More than one starting action may be valid; define an assessment guide before the study.

### RQ2 — Adjusting a schedule

**To what extent can university students with ADHD adjust an AI-proposed coursework schedule to fit their stated availability without assistance?**

Focus: whether students can independently revise the suggested schedule to fit their availability.

- Prototype interaction: inspect a proposed schedule, change a time slot, resolve a conflict, and confirm the revised schedule.
- Example test activity: using a scenario with an existing class and an assignment deadline, move a study session to an available time and save the change.
- Possible evidence: successful completion against the scenario's constraints, errors, time to complete the change, requests for moderator help, and perceived control over the schedule.

### RQ3 — Finding support when stuck

**How easily can university students with ADHD locate and use the prototype's task-support feature to identify a next action when they are unsure how to proceed with a coursework step?**

Focus: whether students can find support and determine a next action when a step is unclear.

- Prototype interaction: open support from the current task, choose to clarify or break down the step, review the simulated suggestion, and return to the updated plan.
- Example test activity: in a prepared scenario, a coursework step is too vague to act on; use the available support to determine a more specific next action.
- Possible evidence: discovery of the support control, successful use of the support flow, ability to explain the next action, time, requests for moderator help, and perceived usefulness. A scripted scenario tests discoverability and interaction; it does not establish that genuine frustration has been reduced.

## UX decisions to test

These are proposed design choices, not established preferences of all students with ADHD:

- Make the next action visible while keeping the full plan accessible.
- Let the user edit and confirm AI suggestions before saving.
- Show schedule conflicts and clear feedback after changes.
- Keep a labelled support control beside the relevant task.
- Update the number of completed steps after a completion action; do not imply that all steps take equal effort.
- Use icons with text labels. Consider light illustrations for onboarding and empty states; avoid placing decorative content in the main planning area unless it serves a clear purpose. Image assets have not yet been generated.

## Basis for the direction

Zhu, Z., Yu, J. and Luo, Y. (2026), *Scaffolding Metacognition with GenAI: Exploring Design Opportunities to Support Task Management for University Students with ADHD*, CHI '26. https://doi.org/10.1145/3772318.3790697

The authors' co-design findings inform the decision to explore editable task decomposition and user control. They do not establish the usability or effectiveness of this proposed prototype. Source and search notes are in `research-question-options.md`.

## Remaining work

- Student reviews and adapts the wording to their own understanding and intended design.
- Inspect the supplied `.rp` when available, then map its existing screens and interactions to these three research directions.
- Task 5 also requires the Axure work completed at the point of submission; this document alone does not satisfy that requirement.
