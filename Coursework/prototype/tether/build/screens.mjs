// Tether — screen definitions.
// Each screen is drawn with Axvg primitives; behaviour is declared as hotspot cases
// that the Python driver resolves to real Axure widgets and interactions.
import { rect, text, frame, composeDesign, hex, circle } from 'file:///E:/Hoc%20tap/Mon%20hoc/N%C4%83m%203%20k%C3%AC%201/COMP1649_HCI/tools/axure-ai/axvg/axvg-build.ts';

export const T = {
  paper: hex('#F7F4ED'),
  shade: hex('#EFEAE0'),
  ink: hex('#171614'),
  muted: hex('#6B6459'),
  hair: hex('#DCD5C7'),
  thread: hex('#B4462F'),
  white: hex('#FFFFFF'),
};

const W = 390, H = 844, M = 28, CW = W - M * 2;

// --- primitives -----------------------------------------------------------
const name = (w, n) => { w.name = n; w.isNameDynamic = false; return w; };
const box = (n, x, y, w, h, fill, opts = {}) =>
  name(rect({ x, y, w, h, fill, corners: opts.r ?? 0, border: opts.border }), n);
const FACE = { 400: 'Inter - Regular', 500: 'Inter - Medium', 600: 'Inter - Semi Bold', 700: 'Inter - Bold' };
const label = (n, x, y, w, h, content, size = 15, color = T.ink, weight = 400, align = 'left') =>
  name(text({ x, y, w, h, content, size, color, weight, typeface: FACE[weight] ?? FACE[400], align }), n);

// a vertical thread that ends in a knot at the current position
const thread = (y0, y1, x = M + 4) => [
  box('thread_line', x, y0, 2, y1 - y0, T.thread),
  name(circle({ x: x - 6, y: y1 - 7, d: 14, fill: T.thread }), 'thread_knot'),
];

const chip = (n, x, y, w, content) => [
  box(`${n}_bg`, x, y, w, 36, T.paper, { r: 18, border: { color: T.hair, thickness: 1 } }),
  label(`${n}_label`, x, y + 9, w, 18, content, 12.5, T.ink, 400, 'center'),
];

const primary = (n, y, content, x = M, w = CW) => [
  box(`${n}_bg`, x, y, w, 56, T.ink, { r: 28 }),
  label(`${n}_label`, x, y + 18, w, 20, content, 15, T.white, 700, 'center'),
];

const secondary = (n, y, content, x = M, w = CW) =>
  label(`${n}_label`, x, y, w, 20, content, 13.5, T.muted, 500, 'center');

const eyebrow = (content) => label('eyebrow', M, 56, CW, 16, content, 11, T.muted, 700);
const display = (content, y = 84, size = 32) => label('display', M, y, CW, size * 1.5, content, size, T.ink, 700);
const lead = (content, y = 148, h = 46) => label('lead', M, y, CW, h, content, 16, T.muted, 400);

const field = (n, y, placeholder) => [
  label(`${n}_label`, M, y - 26, CW, 16, '', 12.5, T.muted, 500),
];

// --- screens --------------------------------------------------------------
const screens = [];

// 00 Start ----------------------------------------------------------------
screens.push({
  id: '00-start', title: '00 Start',
  draw: () => [
    eyebrow('COMP1649 · HCI PROTOTYPE'),
    display('Tether', 88, 44),
    lead('Stop anywhere. Pick up here.', 150, 24),
    label('body', M, 196, CW, 78,
      'A study companion for university students with ADHD. It keeps the thread of what you were doing, so restarting costs nothing.', 14.5, T.muted),
    ...thread(300, 356),

    box('row1_bg', M, 396, CW, 64, T.shade),
    label('row1_no', M + 16, 412, 24, 18, '01', 11, T.thread, 700),
    label('row1_title', M + 16, 428, 220, 20, 'A first session', 15, T.ink, 600),
    label('row1_arrow', M + CW - 40, 420, 24, 20, '→', 16, T.ink, 400, 'right'),

    box('row2_bg', M, 468, CW, 64, T.shade),
    label('row2_no', M + 16, 484, 24, 18, '02', 11, T.thread, 700),
    label('row2_title', M + 16, 500, 220, 20, 'The return visit', 15, T.ink, 600),
    label('row2_arrow', M + CW - 40, 492, 24, 20, '→', 16, T.ink, 400, 'right'),

    box('row3_bg', M, 540, CW, 64, T.shade),
    label('row3_no', M + 16, 556, 24, 18, '03', 11, T.thread, 700),
    label('row3_title', M + 16, 572, 220, 20, 'Getting unstuck', 15, T.ink, 600),
    label('row3_arrow', M + CW - 40, 564, 24, 20, '→', 16, T.ink, 400, 'right'),

    label('researcher', M, 640, CW, 40,
      'Research condition B\nA conventional task list, for comparison', 12, T.muted),
    label('footer', M, 780, CW, 20, 'Axure RP 11 · every screen is interactive', 11, T.muted),
  ],
  hotspots: [
    { name: 'hs_row1', rect: [M, 396, CW, 64] },
    { name: 'hs_row2', rect: [M, 468, CW, 64] },
    { name: 'hs_row3', rect: [M, 540, CW, 64] },
    { name: 'hs_researcher', rect: [M, 636, CW, 46] },
  ],
  interactions: [
    { target: 'hs_row1', cases: [{ name: 'first session', actions: [{ go: '01-home-empty' }] }] },
    { target: 'hs_row2', cases: [{ name: 'return visit', actions: [{ go: '05a-home-thread-a' }] }] },
    { target: 'hs_row3', cases: [{ name: 'stuck', actions: [{ go: '06-stuck' }] }] },
    { target: 'hs_researcher', cases: [{ name: 'baseline', actions: [{ go: '20-baseline-list' }] }] },
  ],
});

// 01 Home, empty ----------------------------------------------------------
screens.push({
  id: '01-home-empty', title: '01 Home empty',
  draw: () => [
    eyebrow('TUESDAY 3 NOVEMBER · 14:06'),
    display('Nothing to pick up yet.', 88, 30),
    lead('That is fine. One thing is enough to start.', 168, 24),
    ...thread(212, 268),

    box('card_bg', M, 320, CW, 132, T.shade),
    label('card_kicker', M + 20, 340, CW - 40, 16, 'NO THREAD', 11, T.muted, 700),
    label('card_body', M + 20, 366, CW - 40, 66,
      'A thread is one sentence about where you stopped. You do not have one yet.', 14, T.muted),

    ...primary('btn_start', 640, 'Name one thing  →'),
    secondary('btn_existing', 716, 'I already have a thread  →'),
    label('footer', M, 780, CW, 20, 'Tether keeps the thread, not the to-do list.', 11, T.muted),
  ],
  hotspots: [
    { name: 'hs_start', rect: [M, 640, CW, 56] },
    { name: 'hs_existing', rect: [M, 708, CW, 36] },
  ],
  interactions: [
    { target: 'hs_start', cases: [{ name: 'start', actions: [{ go: '02-name-it' }] }] },
    { target: 'hs_existing', cases: [{ name: 'existing thread', actions: [{ go: '05a-home-thread-a' }] }] },
  ],
});

// 02 Name it --------------------------------------------------------------
screens.push({
  id: '02-name-it', title: '02 Name it',
  draw: () => [
    eyebrow('FIRST SESSION · 1 OF 3'),
    display('What is the one thing?', 88, 30),
    lead('Not the module. Not the deadline. The thing you keep avoiding.', 150, 46),

    label('field_label', M, 222, CW, 16, 'THE ONE THING', 11, T.muted, 700),
    box('field_bg', M, 244, CW, 56, T.white),

    ...chip('chip_a', M, 320, 168, 'The discussion section'),
    ...chip('chip_b', M + 176, 320, 158, 'The reading list'),
    ...chip('chip_c', M, 364, 150, 'The reference list'),
    ...chip('chip_d', M + 158, 364, 150, 'Marking criteria'),

    label('helper', M, 428, CW, 40, 'Type it, or pick one above.', 13, T.muted),
    ...thread(500, 556),

    ...primary('btn_find', 640, 'Find my first move  →'),
    secondary('btn_back', 716, '←  Back'),
    label('footer', M, 780, CW, 20, 'One thing. Not a plan.', 11, T.muted),
  ],
  inputs: [{ name: 'name_input', rect: [M, 244, CW, 56], placeholder: 'e.g. the discussion section' }],
  hotspots: [
    { name: 'hs_find', rect: [M, 640, CW, 56] },
    { name: 'hs_back', rect: [M, 708, CW, 36] },
    { name: 'hs_chip_a', rect: [M, 320, 168, 36] },
    { name: 'hs_chip_b', rect: [M + 176, 320, 158, 36] },
    { name: 'hs_chip_c', rect: [M, 364, 150, 36] },
    { name: 'hs_chip_d', rect: [M + 158, 364, 150, 36] },
  ],
  interactions: [
    { target: 'hs_chip_a', cases: [{ name: 'chip a', actions: [{ setInput: 'name_input', text: 'the discussion section' }] }] },
    { target: 'hs_chip_b', cases: [{ name: 'chip b', actions: [{ setInput: 'name_input', text: 'the reading list' }] }] },
    { target: 'hs_chip_c', cases: [{ name: 'chip c', actions: [{ setInput: 'name_input', text: 'the reference list' }] }] },
    { target: 'hs_chip_d', cases: [{ name: 'chip d', actions: [{ setInput: 'name_input', text: 'the marking criteria' }] }] },
    {
      target: 'hs_find',
      cases: [
        {
          name: 'nothing typed', when: { input: 'name_input', equals: '' },
          actions: [{ set: 'helper', text: 'Give it a name first. Even three words is enough.', color: 'error' }],
        },
        { name: 'go', actions: [{ go: '03-the-move' }] },
      ],
    },
    { target: 'hs_back', cases: [{ name: 'back', actions: [{ go: '01-home-empty' }] }] },
  ],
});

// 03 The move (with in-page grain reduction) ------------------------------
screens.push({
  id: '03-the-move', title: '03 The move',
  draw: () => [
    eyebrow('YOUR FIRST MOVE · 3 MIN'),
    display('Start here.', 88, 30),
    ...thread(150, 206),

    label('move_text', M + 24, 158, CW - 24, 96,
      'Open the brief and copy the three marking criteria into your document.', 19, T.ink, 500),
    label('why_text', M + 24, 262, CW - 24, 60,
      'You cannot plan an essay against criteria you have not read.', 13.5, T.muted),

    label('grain_note', M, 340, CW, 18, '3 minutes, no more.', 12, T.thread, 600),

    box('rule', M, 380, CW, 1, T.hair),
    label('alt_label', M, 400, CW, 18, 'NOT THE RIGHT MOVE?', 11, T.muted, 700),
    label('alt_move', M, 424, CW, 40, 'Read one page of the brief and highlight one sentence.', 13.5, T.muted),

    ...primary('btn_start', 640, 'Start it  →'),
    secondary('btn_smaller', 712, 'Still too big — make it smaller'),
    secondary('btn_back', 748, '←  Back'),
  ],
  inputs: [{ name: 's_grain', rect: [W - 3, 0, 3, 3], placeholder: '' }],
  hotspots: [
    { name: 'hs_start', rect: [M, 640, CW, 56] },
    { name: 'hs_smaller', rect: [M, 704, CW, 40] },
    { name: 'hs_back', rect: [M, 740, CW, 32] },
  ],
  interactions: [
    {
      target: 'hs_smaller',
      cases: [
        {
          name: 'halve once', when: { input: 's_grain', equals: '' },
          actions: [
            { setInput: 's_grain', text: '1' },
            { set: 'move_text', text: 'Copy just the first marking criterion into your document.' },
            { set: 'why_text', text: 'One criterion is enough to know what the marker wants.' },
            { set: 'grain_note', text: 'Halved — 90 seconds.' },
          ],
        },
        {
          name: 'halve twice', when: { input: 's_grain', equals: '1' },
          actions: [
            { setInput: 's_grain', text: '2' },
            { set: 'move_text', text: 'Open the brief. Find the marking criteria page.' },
            { set: 'why_text', text: 'Opening is the whole job. You can stop after it.' },
            { set: 'grain_note', text: 'Smallest version — 30 seconds.' },
            { set: 'btn_start_label', text: 'Open it  →' },
          ],
        },
        {
          name: 'already smallest',
          actions: [{ set: 'grain_note', text: 'This is as small as it gets. That is the point.' }],
        },
      ],
    },
    { target: 'hs_start', cases: [{ name: 'start', actions: [{ go: '04-ignition' }] }] },
    { target: 'hs_back', cases: [{ name: 'back', actions: [{ go: '02-name-it' }] }] },
  ],
});

// 04 Ignition (3 blocks) --------------------------------------------------
screens.push({
  id: '04-ignition', title: '04 Ignition',
  draw: () => [
    eyebrow('3 MINUTES · STOP AT 14:09'),
    display('Do the move. Nothing else.', 88, 28),
    ...thread(150, 206),

    label('move_text', M + 24, 158, CW - 24, 96,
      'Copy the three marking criteria into your document.', 18, T.ink, 500),

    label('dots', M, 300, CW, 40, '○   ○   ○', 26, T.thread, 400, 'center'),
    label('block_label', M, 348, CW, 18, 'Block 1 of 3', 12, T.muted, 500, 'center'),
    label('block_hint', M, 380, CW, 40,
      'Each block is one minute. You are allowed to stop after three.', 13, T.muted, 400, 'center'),

    ...primary('btn_block', 640, 'Block done  →'),
    secondary('btn_stuck', 712, 'I am stuck'),
    secondary('btn_back', 748, '←  Back to the move'),
  ],
  inputs: [{ name: 's_block', rect: [W - 3, 0, 3, 3], placeholder: '' }],
  hotspots: [
    { name: 'hs_block', rect: [M, 640, CW, 56] },
    { name: 'hs_stuck', rect: [M, 704, CW, 40] },
    { name: 'hs_back', rect: [M, 740, CW, 32] },
  ],
  interactions: [
    {
      target: 'hs_block',
      cases: [
        {
          name: 'block one', when: { input: 's_block', equals: '' },
          actions: [
            { setInput: 's_block', text: '1' },
            { set: 'dots', text: '●   ○   ○' },
            { set: 'block_label', text: 'Block 2 of 3' },
          ],
        },
        {
          name: 'block two', when: { input: 's_block', equals: '1' },
          actions: [
            { setInput: 's_block', text: '2' },
            { set: 'dots', text: '●   ●   ○' },
            { set: 'block_label', text: 'Block 3 of 3' },
          ],
        },
        {
          name: 'block three',
          actions: [
            { set: 'dots', text: '●   ●   ●' },
            { set: 'block_label', text: 'That is the three.' },
            { go: '10-landed' },
          ],
        },
      ],
    },
    { target: 'hs_stuck', cases: [{ name: 'stuck', actions: [{ go: '06-stuck' }] }] },
    { target: 'hs_back', cases: [{ name: 'back', actions: [{ go: '03-the-move' }] }] },
  ],
});

// 06 Stuck ----------------------------------------------------------------
screens.push({
  id: '06-stuck', title: '06 Stuck',
  draw: () => [
    eyebrow('STUCK · THIS IS INFORMATION'),
    display('What kind of stuck?', 88, 30),
    lead('It is not one thing. Pick the one that fits.', 150, 24),

    box('r1_bg', M, 208, CW, 76, T.shade),
    label('r1_title', M + 20, 222, CW - 40, 20, 'I do not know how to start.', 15, T.ink, 500),
    label('r1_sub', M + 20, 246, CW - 40, 18, 'The first step is not visible yet.', 12, T.muted),

    box('r2_bg', M, 296, CW, 76, T.shade),
    label('r2_title', M + 20, 310, CW - 40, 20, 'It is too boring to hold on to.', 15, T.ink, 500),
    label('r2_sub', M + 20, 334, CW - 40, 18, 'Nothing about it is interesting enough.', 12, T.muted),

    box('r3_bg', M, 384, CW, 76, T.shade),
    label('r3_title', M + 20, 398, CW - 40, 20, 'It will not be good enough.', 15, T.ink, 500),
    label('r3_sub', M + 20, 422, CW - 40, 18, 'Starting means finding out it is bad.', 12, T.muted),

    box('resp_bg', M, 490, CW, 116, T.white, { border: { color: T.hair, thickness: 1 } }),
    label('resp_text', M + 20, 510, CW - 40, 84,
      'Pick the one that is closest. You can change it after.', 14, T.muted),

    ...primary('btn_try', 640, 'Try the smaller version  →'),
    secondary('btn_back', 716, '←  Back to the block'),
  ],
  hotspots: [
    { name: 'hs_r1', rect: [M, 208, CW, 76] },
    { name: 'hs_r2', rect: [M, 296, CW, 76] },
    { name: 'hs_r3', rect: [M, 384, CW, 76] },
    { name: 'hs_try', rect: [M, 640, CW, 56] },
    { name: 'hs_back', rect: [M, 708, CW, 36] },
  ],
  interactions: [
    {
      target: 'hs_r1', cases: [{ name: 'cannot start', actions: [
        { set: 'resp_text', text: 'Then the step is still too big. Open the file and read one heading. That is the whole step.' },
      ] }],
    },
    {
      target: 'hs_r2', cases: [{ name: 'too boring', actions: [
        { set: 'resp_text', text: 'Then shrink it until it is over in 90 seconds. Boredom needs a finish line, not willpower.' },
      ] }],
    },
    {
      target: 'hs_r3', cases: [{ name: 'not good enough', actions: [
        { set: 'resp_text', text: 'Then write the bad version on purpose. You cannot edit a page that does not exist.' },
      ] }],
    },
    { target: 'hs_try', cases: [{ name: 'try', actions: [{ go: '07-ninety' }] }] },
    { target: 'hs_back', cases: [{ name: 'back', actions: [{ go: '04-ignition' }] }] },
  ],
});

// 07 Ninety ---------------------------------------------------------------
screens.push({
  id: '07-ninety', title: '07 Ninety seconds',
  draw: () => [
    eyebrow('90 SECONDS'),
    display('Open the file.', 88, 40),
    lead('That is the whole job. You are not writing yet.', 170, 24),
    ...thread(230, 286),

    label('note', M, 330, CW, 60,
      'If you keep going after 90 seconds, that is a bonus, not the plan.', 13.5, T.muted),

    ...primary('btn_done', 640, 'Done  →'),
    secondary('btn_back', 716, '←  Back'),
    label('footer', M, 780, CW, 20, 'The smallest version is still a version.', 11, T.muted),
  ],
  hotspots: [
    { name: 'hs_done', rect: [M, 640, CW, 56] },
    { name: 'hs_back', rect: [M, 708, CW, 36] },
  ],
  interactions: [
    { target: 'hs_done', cases: [{ name: 'done', actions: [{ go: '10-landed' }] }] },
    { target: 'hs_back', cases: [{ name: 'back', actions: [{ go: '06-stuck' }] }] },
  ],
});

// 10 Landed ---------------------------------------------------------------
screens.push({
  id: '10-landed', title: '10 Landed',
  draw: () => [
    eyebrow('THAT IS ONE'),
    display('Block done.', 88, 40),
    lead('You do not need to keep going. You need to know where you stopped.', 170, 46),
    ...thread(250, 306),

    label('note', M, 350, CW, 60,
      'One block counts. The next session starts from here, not from the beginning.', 13.5, T.muted),

    ...primary('btn_thread', 640, 'Leave a thread  →'),
    secondary('btn_new', 716, 'Start something new'),
    label('footer', M, 780, CW, 20, 'Stopping well is part of the work.', 11, T.muted),
  ],
  hotspots: [
    { name: 'hs_thread', rect: [M, 640, CW, 56] },
    { name: 'hs_new', rect: [M, 708, CW, 36] },
  ],
  interactions: [
    { target: 'hs_thread', cases: [{ name: 'thread', actions: [{ go: '08-pause' }] }] },
    { target: 'hs_new', cases: [{ name: 'new', actions: [{ go: '01-home-empty' }] }] },
  ],
});

// 08 Pause point ----------------------------------------------------------
screens.push({
  id: '08-pause', title: '08 Pause point',
  draw: () => [
    eyebrow('BEFORE YOU GO'),
    display('Leave a thread.', 84, 30),
    lead('So that next time costs nothing to restart.', 142, 24),

    label('q1', M, 190, CW, 16, 'WHERE DID YOU STOP?', 10.5, T.muted, 700),
    ...chip('q1a', M, 212, 112, 'Mid-sentence'),
    ...chip('q1b', M + 120, 212, 122, 'On a source'),
    ...chip('q1c', M + 250, 212, 84, 'Just opened'),
    label('v1', M, 256, CW, 18, '—', 13, T.ink, 500),

    label('q2', M, 292, CW, 16, 'NEXT PHYSICAL MOVE?', 10.5, T.muted, 700),
    ...chip('q2a', M, 314, 132, 'Finish the sentence'),
    ...chip('q2b', M + 140, 314, 108, 'Paste the link'),
    ...chip('q2c', M + 256, 314, 78, 'Read page 4'),
    label('v2', M, 358, CW, 18, '—', 13, T.ink, 500),

    label('q3', M, 394, CW, 16, 'HOW LONG NEXT TIME?', 10.5, T.muted, 700),
    ...chip('q3a', M, 416, 84, '3 min'),
    ...chip('q3b', M + 92, 416, 84, '10 min'),
    ...chip('q3c', M + 184, 416, 84, '25 min'),
    label('v3', M, 460, CW, 18, '—', 13, T.ink, 500),

    label('error', M, 512, CW, 40, 'All three, or the thread is not much use.', 12.5, T.muted),

    ...primary('btn_tie', 640, 'Tie it off  →'),
    secondary('btn_close', 716, 'Close without a thread'),
  ],
  inputs: [
    { name: 's_q1', rect: [W - 3, 0, 3, 3], placeholder: '' },
    { name: 's_q2', rect: [W - 3, 0, 3, 3], placeholder: '' },
    { name: 's_q3', rect: [W - 3, 0, 3, 3], placeholder: '' },
  ],
  hotspots: [
    { name: 'hs_q1a', rect: [M, 212, 112, 36] },
    { name: 'hs_q1b', rect: [M + 120, 212, 122, 36] },
    { name: 'hs_q1c', rect: [M + 250, 212, 84, 36] },
    { name: 'hs_q2a', rect: [M, 314, 132, 36] },
    { name: 'hs_q2b', rect: [M + 140, 314, 108, 36] },
    { name: 'hs_q2c', rect: [M + 256, 314, 78, 36] },
    { name: 'hs_q3a', rect: [M, 416, 84, 36] },
    { name: 'hs_q3b', rect: [M + 92, 416, 84, 36] },
    { name: 'hs_q3c', rect: [M + 184, 416, 84, 36] },
    { name: 'hs_tie', rect: [M, 640, CW, 56] },
    { name: 'hs_close', rect: [M, 708, CW, 36] },
  ],
  interactions: [
    { target: 'hs_q1a', cases: [{ name: 'q1a', actions: [{ setInput: 's_q1', text: 'mid' }, { set: 'v1', text: 'Mid-sentence, in the discussion section.' }] }] },
    { target: 'hs_q1b', cases: [{ name: 'q1b', actions: [{ setInput: 's_q1', text: 'source' }, { set: 'v1', text: 'Waiting on a source you have not found.' }] }] },
    { target: 'hs_q1c', cases: [{ name: 'q1c', actions: [{ setInput: 's_q1', text: 'open' }, { set: 'v1', text: 'You only opened the file.' }] }] },
    { target: 'hs_q2a', cases: [{ name: 'q2a', actions: [{ setInput: 's_q2', text: 'sentence' }, { set: 'v2', text: 'Finish the sentence you started.' }] }] },
    { target: 'hs_q2b', cases: [{ name: 'q2b', actions: [{ setInput: 's_q2', text: 'link' }, { set: 'v2', text: 'Paste the source link into the notes.' }] }] },
    { target: 'hs_q2c', cases: [{ name: 'q2c', actions: [{ setInput: 's_q2', text: 'page' }, { set: 'v2', text: 'Read page 4 and mark one line.' }] }] },
    { target: 'hs_q3a', cases: [{ name: 'q3a', actions: [{ setInput: 's_q3', text: '3' }, { set: 'v3', text: '3 minutes.' }] }] },
    { target: 'hs_q3b', cases: [{ name: 'q3b', actions: [{ setInput: 's_q3', text: '10' }, { set: 'v3', text: '10 minutes.' }] }] },
    { target: 'hs_q3c', cases: [{ name: 'q3c', actions: [{ setInput: 's_q3', text: '25' }, { set: 'v3', text: '25 minutes.' }] }] },
    {
      target: 'hs_tie',
      cases: [
        { name: 'no q1', when: { input: 's_q1', equals: '' }, actions: [{ set: 'error', text: 'Where did you stop? One chip is enough.' }] },
        { name: 'no q2', when: { input: 's_q2', equals: '' }, actions: [{ set: 'error', text: 'What is the next physical move? Without it there is no thread.' }] },
        { name: 'no q3', when: { input: 's_q3', equals: '' }, actions: [{ set: 'error', text: 'How long will it take next time? Guess small.' }] },
        { name: 'thread a', when: { input: 's_q2', equals: 'sentence' }, actions: [{ go: '05a-home-thread-a' }] },
        { name: 'thread b', when: { input: 's_q2', equals: 'link' }, actions: [{ go: '05b-home-thread-b' }] },
        { name: 'thread c', actions: [{ go: '05c-home-thread-c' }] },
      ],
    },
    { target: 'hs_close', cases: [{ name: 'close', actions: [{ go: '01-home-empty' }] }] },
  ],
});

// 05a/b/c Home with thread ------------------------------------------------
const homeThread = (id, title, stopped, nextMove, time, stamp) => screens.push({
  id, title,
  draw: () => [
    eyebrow('NEXT TIME YOU OPEN TETHER'),
    display('You were here.', 88, 30),
    lead('Nothing to reconstruct. It is already written down.', 142, 24),
    ...thread(196, 252),

    box('card_bg', M, 286, CW, 208, T.shade),
    label('card_k1', M + 20, 306, CW - 40, 14, 'WHERE YOU STOPPED', 10, T.muted, 700),
    label('card_v1', M + 20, 324, CW - 40, 40, stopped, 14, T.ink, 500),
    label('card_k2', M + 20, 376, CW - 40, 14, 'NEXT MOVE', 10, T.muted, 700),
    label('card_v2', M + 20, 394, CW - 40, 44, nextMove, 14, T.ink, 500),
    label('card_k3', M + 20, 446, 120, 14, 'TIME', 10, T.muted, 700),
    label('card_v3', M + 20, 464, 120, 18, time, 13, T.ink, 500),
    label('card_stamp', M + 20, 446, CW - 40, 14, stamp, 10, T.muted, 400, 'right'),

    ...primary('btn_pick', 640, 'Pick it up  →'),
    secondary('btn_newthread', 716, 'That is not it — leave a new thread'),
    label('footer', M, 780, CW, 20, 'One thread at a time. That is the whole method.', 11, T.muted),
  ],
  hotspots: [
    { name: 'hs_pick', rect: [M, 640, CW, 56] },
    { name: 'hs_newthread', rect: [M, 708, CW, 36] },
  ],
  interactions: [
    { target: 'hs_pick', cases: [{ name: 'pick up', actions: [{ go: '07-ninety' }] }] },
    { target: 'hs_newthread', cases: [{ name: 'new thread', actions: [{ go: '08-pause' }] }] },
  ],
});

homeThread('05a-home-thread-a', '05a Home thread A',
  'Mid-sentence, in the discussion section.',
  'Finish the sentence you started.', '3 minutes.', 'Tied off Tuesday, 14:09');
homeThread('05b-home-thread-b', '05b Home thread B',
  'Waiting on a source you have not found.',
  'Paste the source link into the notes.', '10 minutes.', 'Tied off Tuesday, 14:09');
homeThread('05c-home-thread-c', '05c Home thread C',
  'You only opened the file.',
  'Read page 4 and mark one line.', '25 minutes.', 'Tied off Tuesday, 14:09');

// 20 Baseline list (research condition B) ---------------------------------
screens.push({
  id: '20-baseline-list', title: '20 Baseline list',
  draw: () => [
    eyebrow('COMP1649 · COURSEWORK'),
    display('Your tasks', 84, 30),
    lead('6 tasks · 3 due this week', 142, 24),

    box('progress_bg', M, 186, CW, 6, T.hair),
    box('progress_fill', M, 186, 112, 6, T.ink),
    label('progress_label', M, 200, CW, 16, '1 of 6 complete', 11, T.muted),

    box('t1_bg', M, 236, CW, 56, T.white, { border: { color: T.hair, thickness: 1 } }),
    label('t1_text', M + 16, 254, CW - 32, 20, '☐  Read the brief', 14, T.ink),
    box('t2_bg', M, 296, CW, 56, T.white, { border: { color: T.hair, thickness: 1 } }),
    label('t2_text', M + 16, 314, CW - 32, 20, '☐  Draft the discussion section', 14, T.ink),
    box('t3_bg', M, 356, CW, 56, T.white, { border: { color: T.hair, thickness: 1 } }),
    label('t3_text', M + 16, 374, CW - 32, 20, '☐  Find two sources', 14, T.ink),
    box('t4_bg', M, 416, CW, 56, T.white, { border: { color: T.hair, thickness: 1 } }),
    label('t4_text', M + 16, 434, CW - 32, 20, '☐  Write the introduction', 14, T.ink),
    box('t5_bg', M, 476, CW, 56, T.white, { border: { color: T.hair, thickness: 1 } }),
    label('t5_text', M + 16, 494, CW - 32, 20, '☐  Check against the rubric', 14, T.ink),
    box('t6_bg', M, 536, CW, 56, T.white, { border: { color: T.hair, thickness: 1 } }),
    label('t6_text', M + 16, 554, CW - 32, 20, '☐  Proofread', 14, T.ink),

    label('note', M, 620, CW, 60,
      'Condition B. A competent task list: everything visible at once, nothing decided for you.', 12, T.muted),

    ...primary('btn_study', 700, 'Start studying  →'),
    secondary('btn_back', 768, '←  Back to Tether'),
  ],
  hotspots: [
    { name: 'hs_t2', rect: [M, 296, CW, 56] },
    { name: 'hs_study', rect: [M, 700, CW, 56] },
    { name: 'hs_back', rect: [M, 760, CW, 32] },
  ],
  interactions: [
    { target: 'hs_t2', cases: [{ name: 'open task', actions: [{ go: '21-baseline-item' }] }] },
    { target: 'hs_study', cases: [{ name: 'study', actions: [{ go: '21-baseline-item' }] }] },
    { target: 'hs_back', cases: [{ name: 'back', actions: [{ go: '00-start' }] }] },
  ],
});

// 21 Baseline item --------------------------------------------------------
screens.push({
  id: '21-baseline-item', title: '21 Baseline item',
  draw: () => [
    eyebrow('TASK · DUE IN 3 DAYS'),
    display('Draft the discussion section', 84, 26),
    lead('Estimated 90 minutes · 4 steps', 142, 24),

    label('steps', M, 196, CW, 120,
      '1.  Re-read the notes\n2.  Outline the argument\n3.  Draft 400 words\n4.  Edit and cut', 14, T.ink),

    box('note_bg', M, 340, CW, 92, T.shade),
    label('note', M + 20, 360, CW - 40, 56,
      'Linked to: the rubric, two sources, the reading list.', 13, T.muted),

    ...primary('btn_done', 640, 'Mark as done'),
    secondary('btn_back', 716, '←  Back to tasks'),
  ],
  hotspots: [
    { name: 'hs_done', rect: [M, 640, CW, 56] },
    { name: 'hs_back', rect: [M, 708, CW, 36] },
  ],
  interactions: [
    { target: 'hs_done', cases: [{ name: 'done', actions: [{ go: '20-baseline-list' }] }] },
    { target: 'hs_back', cases: [{ name: 'back', actions: [{ go: '20-baseline-list' }] }] },
  ],
});

// --- render ---------------------------------------------------------------
export function build() {
  return screens.map((s) => ({
    id: s.id,
    title: s.title,
    json: composeDesign(frame({ name: s.title, w: W, h: H, bg: T.paper, children: s.draw() })),
    inputs: s.inputs ?? [],
    hotspots: s.hotspots ?? [],
    interactions: s.interactions ?? [],
  }));
}

export const meta = { W, H, M, CW };
