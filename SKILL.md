---
name: codewalk
description: Turn any codebase into a personal, branching, narrated interactive HTML course. Use when the user says "turn this into a course," "walk me through this codebase," "teach me how this code works," "make me a codewalk," or similar.
---

# Generation flow

Follow these steps in order. Each step references a file in `references/` — read
it before executing that step.

## 1. Intake

Read `references/personalization.md`. Ask the four intake questions as one short
batch. If the user's original request already answered some, skip those. If they
say nothing, default to Orient / no prior knowledge / no narration / 20 min and
state what you assumed in one line.

## 2. Check for previous course

Look for a `*.course.json` sidecar next to any existing `*.course.html` for this
repo. If found, read `references/diff-mode.md` and follow the diff protocol
instead of continuing to step 3. If not found, continue.

## 3. Map the codebase

Read `references/codebase-mapping.md`. Find the entry point, trace one real user
action end-to-end, identify 5-9 concepts. Attach a shape category to each concept
as you go (see step 5). The learner's stated goal from intake determines which
action to trace and which concepts to foreground.

## 4. Route into a branch

Read `references/branching-paths.md`. Based on the learner's goal:
- "Debug" / fixing something → Debug path
- "Add" / "change" / building something → Extend path
- Open-ended / "just understand" → Orient path (default)

The path determines concept ordering, depth per concept, and tone. Follow the
spec in branching-paths.md — don't default to Orient ordering for all three.

## 5. Classify and draw metaphors

Read `references/metaphor-bank.md`. For each concept in the map:
1. Classify its shape (Gate, Queue, Cache, Broadcast, Lookup, Pipeline,
   Boundary, Ledger, Scheduler — or mint a new one).
2. Pick a surface metaphor from the codebase's own domain.
3. Check against metaphors already used in this course — no repeats at the
   surface level within one course.

## 6. Build the HTML

Read `references/design-system.md` and `references/interactive-elements.md`.
Build one self-contained HTML file:

- Inline all CSS and JS. No external requests. No CDN. Works offline.
- Domain-matched palette and typography — not a generic theme.
- Scroll-based modules, one per concept, in the order the branch dictates.
- Every module needs: a shape icon, a metaphor block, a code↔English
  translation with real code linked to the source, and either a visualization
  or a quiz (most modules should have both).
- Use at least two of the three animation patterns (data flow, component
  conversation, architecture build-up). Wire all animations to
  IntersectionObserver — never autoplay on page load.
- Quiz wrong answers trigger a simpler follow-up question (see
  interactive-elements.md), not just an answer reveal.
- Quiz answers write state to both localStorage and an embedded
  `<script type="application/json" id="quiz-state">` block (see diff-mode.md).
- Include a "Copy my progress" button in the footer.
- Branch switcher in the top bar: Debug / Extend / Orient.
- End with a "What was left out" section naming cut concepts and why.
- File path above each code snippet links to the exact GitHub blob URL with
  line anchors when the repo has a remote.

## 7. Narration (optional)

If the learner opted in at intake, read `references/narration.md`. Write the
script and sync map. Embed both in the HTML as JSON. Add a collapsible
"Narration" toggle per module for reading the script when no audio is wired up.

## 8. Save course state

Write the `.course.json` sidecar next to the HTML. Schema is in
`references/diff-mode.md`. Include: repo snapshot (commit/hash, entry points,
concepts covered with file lists), learner profile, empty quiz_results object
(populated by the HTML as the learner answers).

## 9. Hand back

Tell the user where the file is and roughly how long it takes to go through.
Don't summarize the course contents — the course does that itself.

---

# Rules

- **One HTML file.** No build step. No separate CSS/JS files. Double-click to open.
- **Original code only.** Every code snippet is an exact, unmodified copy from the
  repo. Never simplify, shorten, or pseudocode a real snippet.
- **50%+ visual per screen.** If it could be a diagram, animation, or interactive
  element, it should not be a paragraph.
- **Quizzes test application, not recall.** No "what does X stand for" questions.
- **No recycled metaphors.** Enforced by shape classification. Never use "bouncer
  for auth," "librarian for lookup," "post office for messaging," or "traffic cop
  for routing."
- **Teach to the goal, not the map.** The course covers what the learner's stated
  goal needs. Say what was cut and why.
- **prefers-reduced-motion.** Every animation has a static fallback.
- **Light and dark mode.** CSS custom properties at `:root`, redefined under
  `@media (prefers-color-scheme: dark)`.

---

# Reference files

Read each one when the step above says to — don't front-load all of them.

| File | Covers |
|---|---|
| `references/personalization.md` | Intake questions, defaults, how answers reshape generation |
| `references/diff-mode.md` | Course state JSON schema, change classification, addendum rules, quiz state persistence |
| `references/codebase-mapping.md` | Finding entry points, tracing actions, selecting and cutting concepts |
| `references/branching-paths.md` | What Debug/Extend/Orient teach differently — ordering, depth, tone, quiz focus |
| `references/metaphor-bank.md` | Shape taxonomy, domain-flavor guidance, no-repeat enforcement, retired clichés |
| `references/design-system.md` | Palette, typography, layout, motion, technical constraints |
| `references/interactive-elements.md` | Quizzes, animations, shape icons, code blocks, glossary, branch switcher UI |
| `references/narration.md` | Script style, sync map format, degradation without audio |

---

# Attribution

The core idea — turning a codebase into a single-file interactive HTML course
with scroll-based modules, code-to-English translations, animated visualizations,
and application-testing quizzes — comes from
[codebase-to-course](https://github.com/zarazhangrui/codebase-to-course) by
[Zara Zhang](https://x.com/zarazhangrui). This skill reimplements that idea
with five additions: personalized intake, diff mode, a structured metaphor bank,
opt-in narration, and branching paths.
