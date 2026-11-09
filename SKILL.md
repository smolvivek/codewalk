---
name: codewalk
description: Turn any codebase into a personal, interactive walkthrough as a single HTML file. Use when the user says "walk me through this codebase," "turn this into a walkthrough," "teach me how this code works," "make me a codewalk," "explain this PR," "what did my agent change," or asks to update an existing one.
---

# Generation flow

Follow these steps in order. Each step names a file in `references/`. Read it
before doing that step.

## 1. Intake

Read `references/personalization.md` and `references/expertise-levels.md`. Ask
the intake questions in one short message. The first question is the reader's
expertise level, which defaults to `vibe`. Skip anything the request already
answered. If the user gives no answers, assume `vibe` level, Orient path, no
narration, 20 minutes, and state that assumption in one line.

## 2. Check for a previous walkthrough

Look for a `*.walkthrough.json` file next to an existing `*.walkthrough.html` for
this repo. If one exists, read `references/diff-mode.md` and follow the diff
protocol instead of continuing to step 3. Otherwise continue.

## 3. Map the codebase

Read `references/codebase-mapping.md`. Find the entry point, trace one real user
action end to end, and pick 5 to 9 concepts. Attach a shape to each concept as
you go (see step 5). The reader's goal from intake decides which action to trace
and which concepts to put first.

## 4. Route into a branch

Read `references/branching-paths.md`. Pick the branch from the reader's goal:

- Fixing something: Debug
- Adding or changing something: Extend
- Open-ended or "just understand": Orient (the default)

The branch sets concept order, depth per concept, and tone. Follow the spec in
that file for the chosen branch.

## 5. Classify and draw metaphors

Read `references/metaphor-bank.md`. For each concept:

1. Classify its shape: Gate, Queue, Cache, Broadcast, Lookup, Pipeline, Boundary,
   Ledger, or Scheduler. Add a new shape if none fits.
2. Pick a surface metaphor from the codebase's own domain.
3. Check it against the metaphors already used in this walkthrough. No repeats.

## 6. Observe

Read `references/ground-truth.md`. Run the traced action in a scratch copy of the
repo and record what happens. If it cannot be run, mark every module Read and
continue. Every module carries an Observed or Read badge.

## 7. Build the HTML

Read `references/design-system.md`, `references/interactive-elements.md`, and
`references/learning-loop.md`. Build one self-contained HTML file:

- Inline all CSS and JS. No external requests, no CDN. It works offline.
- Use a palette and type pairing chosen for this codebase's domain.
- One scroll module per concept, in the order the branch dictates.
- Every module follows the learning loop: Frame, Predict, Reveal, Explain, and
  Apply where the concept touches the reader's goal. The metaphor never appears
  before the prediction.
- Every module has a shape icon, a provenance badge (Observed or Read), a code
  and plain-English pair using real code linked to its source, and a
  visualization.
- Use at least two of the three animation patterns. Trigger every animation with
  an IntersectionObserver, never on page load.
- A wrong prediction or apply answer leads to a simpler follow-up question.
- Write progress (prediction, apply, confidence per concept) to localStorage and
  to an embedded `<script type="application/json" id="quiz-state">` block (see
  `diff-mode.md`).
- Put a "Copy my progress" button in the footer.
- Put a Debug / Extend / Orient switcher in the top bar.
- End with a "Where your picture was off" section listing confident misses, then
  a "What was left out" section naming each cut concept and why.
- Link each snippet's file path to the GitHub blob URL with line anchors when the
  repo has a remote.
- At `new`, `vibe`, and `learner` levels, each module has a collapsed "Go deeper"
  block written for the next level up.
- The first line of the page states the expertise level, assumed goal, and how to
  ask for a rebuild.

## 8. Plan and brief

Read `references/agent-brief.md`. Add the closing module: the reader writes their
plan, then sees the reference plan and a copyable agent brief built from the
concept map and their progress.

## 9. Narration (optional)

If the reader opted in, read `references/narration.md`. Write the script and sync
map, embed both in the HTML as JSON, and add a collapsible narration toggle to
each module. Include a "pause and make a guess" cue before each predict step.

## 10. Save state

Write the `.walkthrough.json` file next to the HTML. The schema is in
`references/diff-mode.md`. Include the repo snapshot (commit or content hash,
entry points, concepts with their files), the reader profile (including level),
and an empty progress object that the page fills in as the reader answers.

## 11. Verify

Run `scripts/verify_walkthrough.py` against the generated HTML and the repo.
Fix anything it flags before handing back.

## 12. Hand back

Tell the user where the file is and about how long it takes to read. Do not
summarize its contents.

---

# Change mode

When the request is about a diff, a PR, or "what did my agent change," read
`references/change-mode.md` and follow that process instead of the generation
flow above. Change mode uses the same learning loop but groups changes by
behavior, not by file, and ends with a verdict and findings instead of a plan
and brief. Output is `{repo}.changes.html`.

---

# Rules

- **One HTML file.** No build step, no separate CSS or JS files. Double-click to
  open.
- **Original code only.** Every snippet is an exact, unmodified copy from the
  repo. Never shorten, simplify, or rewrite a snippet as pseudocode.
- **Predict before explain.** Every module asks the reader to commit to an answer
  before revealing what happens. The metaphor never comes before the prediction.
- **Provenance on every module.** Observed means it was run and recorded. Read
  means it was explained from the code. Nothing in between.
- **Mostly visual.** If something can be a diagram, animation, or interactive
  element, do not write it as a paragraph.
- **No recycled metaphors.** Shape classification enforces this. Never use a
  bouncer for auth, a librarian for lookup, a post office for messaging, or a
  traffic cop for routing.
- **Teach to the goal.** Cover what the reader's goal needs, and say what was cut
  and why.
- **No emoji.** Not in the page, the narration, or the quiz feedback. Shape icons
  are inline SVG.
- **No gamification.** No timers, streaks, points, or numeric scores.
- **Reduced motion.** Every animation has a static fallback under
  `prefers-reduced-motion`.
- **Light and dark mode.** Define colors as CSS custom properties at `:root` and
  redefine them under `@media (prefers-color-scheme: dark)`.
- **Level sets the language.** At `new` and `vibe`, behavior before syntax. At
  `engineer`, skip definitions and lead with design decisions. See
  `references/expertise-levels.md`.

---

# Reference files

Read each file when its step says to. Do not load them all up front.

| File | Covers |
|---|---|
| `references/personalization.md` | Intake questions, defaults, how answers change the build |
| `references/expertise-levels.md` | The four reader levels, what each changes, rules at every level |
| `references/diff-mode.md` | State file schema, change classification, addendum rules, progress storage |
| `references/codebase-mapping.md` | Finding entry points, tracing an action, choosing and cutting concepts |
| `references/branching-paths.md` | How Debug, Extend, and Orient differ in order, depth, tone, and predictions |
| `references/metaphor-bank.md` | Shape list, domain flavor, no-repeat rule, retired metaphors |
| `references/learning-loop.md` | Frame, Predict, Reveal, Explain, Apply loop; confidence; scoring; rules |
| `references/ground-truth.md` | Observed vs Read, how to run, ask-before-running, trace schema, redaction |
| `references/agent-brief.md` | Plan-then-compare, reference plan, copyable agent brief, rules |
| `references/change-mode.md` | Diff intake, grouping by behavior, shape risk table, verdict and findings |
| `references/design-system.md` | Palette, typography, layout, motion, provenance badge, technical limits |
| `references/interactive-elements.md` | Predictions, animations, shape icons, code blocks, glossary, switcher |
| `references/narration.md` | Script style, sync map format, predict-step cues, behavior without audio |
| `scripts/verify_walkthrough.py` | Post-build validation: provenance, traces, credentials, paths, lint |

---

# Attribution

The core idea, turning a codebase into a single-file interactive HTML page with
scroll-based modules, code-to-English translations, and animated visualizations,
comes from [codebase-to-course](https://github.com/zarazhangrui/codebase-to-course)
by [Zara Zhang](https://x.com/zarazhangrui). This skill adds: personalized intake
with four expertise levels, a predict-before-reveal learning loop, observed-versus-read
provenance from a real run, a plan-then-brief closing module, diff mode, change mode,
a structured metaphor bank, opt-in narration, and branching paths.
