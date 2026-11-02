// Spike 01 — verify the Tether visual + interaction stack before building 12 pages.
// Checks: Axvg render, ungrouped children addressable, styled dynamic text,
// invisible hotspot, native input appearance, conditional navigation.
import { writeFileSync } from 'node:fs';
import { rect, text, frame, composeDesign, hex, circle } from 'file:///E:/Hoc%20tap/Mon%20hoc/N%C4%83m%203%20k%C3%AC%201/COMP1649_HCI/tools/axure-ai/axvg/axvg-build.ts';

const PAPER = hex('#F7F4ED');
const INK = hex('#171614');
const MUTED = hex('#6B6459');
const HAIR = hex('#DCD5C7');
const THREAD = hex('#B4462F');
const WHITE = hex('#FFFFFF');

const named = (w, name) => { w.name = name; w.isNameDynamic = false; return w; };

const design = composeDesign(
  frame({
    name: 'Spike 01',
    w: 390,
    h: 844,
    bg: PAPER,
    children: [
      named(text({ x: 32, y: 56, w: 326, h: 18, content: 'SPIKE 01 · STACK CHECK', size: 12, color: MUTED, weight: 700 }), 'eyebrow'),

      named(text({ x: 32, y: 88, w: 326, h: 44, content: 'Pick it up.', size: 34, color: INK, weight: 700 }), 'headline'),

      // the thread: one 2px line ending in a knot
      named(rect({ x: 36, y: 160, w: 2, h: 116, fill: THREAD }), 'thread_line'),
      named(circle({ x: 30, y: 276, d: 14, fill: THREAD }), 'thread_knot'),

      // dynamic text target — must keep Inter/size/colour after setText
      named(text({ x: 60, y: 166, w: 298, h: 56, content: 'Finish the sentence you started, then stop.', size: 17, color: INK }), 'move_text'),
      named(text({ x: 60, y: 232, w: 298, h: 18, content: '3 min · COMP1649', size: 13, color: MUTED }), 'move_meta'),

      named(text({ x: 32, y: 348, w: 326, h: 18, content: 'Where did you stop?', size: 13, color: MUTED, weight: 500 }), 'q1_label'),
      named(rect({ x: 32, y: 372, w: 326, h: 52, fill: WHITE, border: { color: HAIR, thickness: 1 }, corners: 10 }), 'q1_field'),

      named(text({ x: 32, y: 448, w: 326, h: 18, content: 'Next physical move?', size: 13, color: MUTED, weight: 500 }), 'q2_label'),
      named(rect({ x: 32, y: 472, w: 326, h: 52, fill: WHITE, border: { color: HAIR, thickness: 1 }, corners: 10 }), 'q2_field'),

      // chips: pill shapes, clickable via hotspots
      named(rect({ x: 32, y: 546, w: 152, h: 36, fill: PAPER, border: { color: HAIR, thickness: 1 }, corners: 18 }), 'chip_a'),
      named(text({ x: 32, y: 555, w: 152, h: 18, content: 'Mid-sentence', size: 13, color: INK, align: 'center' }), 'chip_a_label'),
      named(rect({ x: 194, y: 546, w: 164, h: 36, fill: PAPER, border: { color: HAIR, thickness: 1 }, corners: 18 }), 'chip_b'),
      named(text({ x: 194, y: 555, w: 164, h: 18, content: 'Waiting on a source', size: 13, color: INK, align: 'center' }), 'chip_b_label'),

      // primary action — a designed pill; the real click comes from an invisible hotspot
      named(rect({ x: 32, y: 700, w: 326, h: 56, fill: INK, corners: 28 }), 'primary_bg'),
      named(text({ x: 32, y: 718, w: 326, h: 20, content: 'Tie it off  →', size: 15, color: WHITE, weight: 700, align: 'center' }), 'primary_label'),

      named(text({ x: 32, y: 780, w: 326, h: 18, content: 'Tether · prototype spike', size: 11, color: MUTED }), 'footer'),
    ],
  })
);

writeFileSync(new URL('./spike.axvg.json', import.meta.url), '// axvg\n' + JSON.stringify(design));
console.log('wrote spike.axvg.json', JSON.stringify(design).length, 'bytes');
