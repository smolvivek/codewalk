---
name: codewalk
description: Turn any codebase into a personal, interactive walkthrough as a single HTML file. Use when the user says "walk me through this codebase," "turn this into a walkthrough," "teach me how this code works," "make me a codewalk," or asks to update an existing one.
---

# Generation flow

Follow these steps in order. Each step names a file in `references/`. Read it
before doing that step.

## 1. Intake

Read `references/personalization.md`. Ask the four intake questions in one short
message. Skip any the request already answered. If the user gives no answers,
assume Orient path, no prior knowledge, no narration, 20 minutes, and state that
assumption in one line.

## 2. Check for a previous walkthrough

Look for a `*.walkthrough.json` file next to an existing `*.walkthrough.html` for
this repo. If one exists, read `references/diff-mode.md` and follow the diff
protocol instead of continuing to step 3. Otherwise continue.

## 3. Map the codebase

Read `references/codebase-mapping.md`. Find the entry point, trace one real user
action end to end, and pick 5 to 9 concepts. Attach a shape to each concept as you
go (see step 5). The reader's goal from intake decides which action to trace and
which concepts to put first.

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

## 6. Build the HTML

Read `references/design-system.md` and `references/interactive-elements.md`. Build
one self-contained HTML file:

- Inline all CSS and JS. No external requests, no CDN. It must work offline.
- Use a palette and type pairing chosen for this codebase's domain.
- One scroll module per concept, in the order the branch dictates.
- Every module has a shape icon, a metaphor block, a code and plain-English pair
  using real code linked to its source, and a visualization, a quiz, or both.
- Use at least two of the three animation patterns. Trigger every animation with
  an IntersectionObserver, never on page load.
- A wrong quiz answer leads to a simpler follow-up question, as described in
  `interactive-elements.md`.
- Write quiz results to localStorage and to an embedded
  `<script type="application/json" id="quiz-state">` block (see `diff-mode.md`).
- Put a "Copy my progress" button in the footer.
- Put a Debug / Extend / Orient switcher in the top bar.
- End with a "What was left out" section that names each cut concept and why.
- Link each snippet's file path to the GitHub blob URL with line anchors when the
  repo has a remote.

## 7. Narration (optional)

If the reader opted in, read `references/narration.md`. Write the script and sync
map, embed both in the HTML as JSON, and add a collapsible narration toggle to each
module.

## 8. Save state

Write the `.walkthrough.json` file next to the HTML. The schema is in
`references/diff-mode.md`. Include the repo snapshot (commit or content hash, entry
points, concepts with their files), the reader profile, and an empty `quiz_results`
object that the page fills in as the reader answers.

## 9. Hand back

Tell the user where the file is and about how long it takes to read. Do not
summarize its contents.

---

# Rules

- **One HTML file.** No build step, no separate CSS or JS files. Double-click to open.
- **Original code only.** Every snippet is an exact, unmodified copy from the repo.
  Never shorten, simplify, or rewrite a snippet as pseudocode.
- **Mostly visual.** If something can be a diagram, animation, or interactive
  element, do not write it as a paragraph.
- **Quizzes test application.** No questions about what an acronym stands for.
- **No recycled metaphors.** Shape classification enforces this. Never use a
  bouncer for auth, a librarian for lookup, a post office for messaging, or a
  traffic cop for routing.
- **Teach to the goal.** Cover what the reader's goal needs, and say what was cut
  and why.
- **No emoji.** Not in the page, the narration, or the quiz feedback. Shape icons
  are inline SVG.
- **Reduced motion.** Every animation has a static fallback under
  `prefers-reduced-motion`.
- **Light and dark mode.** Define colors as CSS custom properties at `:root` and
  redefine them under `@media (prefers-color-scheme: dark)`.

---

# Reference files

Read each file when its step says to. Do not load them all up front.

| File | Covers |
|---|---|
| `references/personalization.md` | Intake questions, defaults, how answers change the build |
| `references/diff-mode.md` | State file schema, change classification, addendum rules, quiz state storage |
| `references/codebase-mapping.md` | Finding entry points, tracing an action, choosing and cutting concepts |
| `references/branching-paths.md` | How Debug, Extend, and Orient differ in order, depth, tone, and quizzes |
| `references/metaphor-bank.md` | Shape list, domain flavor, no-repeat rule, retired metaphors |
| `references/design-system.md` | Palette, typography, layout, motion, technical limits |
| `references/interactive-elements.md` | Quizzes, animations, shape icons, code blocks, glossary, branch switcher |
| `references/narration.md` | Script style, sync map format, behavior without audio |

---

# Attribution

The core idea, turning a codebase into a single-file interactive HTML page with
scroll-based modules, code-to-English translations, animated visualizations, and
application-testing quizzes, comes from
[codebase-to-course](https://github.com/zarazhangrui/codebase-to-course) by
[Zara Zhang](https://x.com/zarazhangrui). This skill reimplements that idea with
five additions: personalized intake, diff mode, a structured metaphor bank, opt-in
narration, and branching paths.
