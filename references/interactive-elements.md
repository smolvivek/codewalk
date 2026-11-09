# Interactive elements

## Quizzes

Test application, never recall.

- Bad: "What does API stand for?"
- Good: "A user reports stale data after switching pages. Based on what you just
  saw about the cache module, where would you look first?"

Each quiz question should be answerable only by someone who understood the
*mechanism* just taught, not someone who memorized a term from the paragraph above
it. Multiple choice is fine; include at least one plausible wrong answer that
reflects a common real misunderstanding of the mechanism (not a joke answer).

Give immediate feedback with a one-line explanation of *why*, tied back to the
specific code/diagram the module just showed — not a generic "correct!"/"try again."

A wrong answer doesn't just reveal the right one. Follow it with one simpler,
more concrete question that isolates the specific misunderstanding the wrong
choice implied, before moving on — a real second attempt, not just an answer key.

## Animated visualizations

Three recurring patterns. A course should use more than one of them — reaching
for the same pattern every time is the animated equivalent of a recycled metaphor.

1. **Data flow** — an element (dot, packet, request) visibly moves through labeled
   stages, pausing briefly at each one with a one-line caption. Good for pipelines,
   middleware chains, request lifecycles.
2. **Component conversation** — chat-bubble exchange between two or more named
   components, each bubble tied to a real function call (shown on tap/hover: the
   actual line of code that message represents). Good for anything shaped like
   request/response, pub/sub, or API calls between services.
3. **Architecture build-up** — a diagram that constructs itself piece by piece as
   the module's text progresses (scroll-linked or step-linked), rather than
   appearing all at once. Good for "here's how the pieces fit together" modules.

**Trigger on scroll, not on load.** Wire every animation to an IntersectionObserver
(or equivalent) on its own module, not a fixed timer from page load — a learner
who's still reading the intro when a module three screens down autoplays never
sees it happen. Each animation plays once when its module enters view, and is
always replayable (a small restart control) and skippable (reduced motion /
"skip to end state" always available).

## Shape icons

Each module carries a small glyph next to its title marking the metaphor-bank
shape it teaches (gate, ledger, pipeline, queue, cache, broadcast, lookup,
boundary, scheduler — see `metaphor-bank.md`). This is what turns "no recycled
metaphors" from something explained in the text into something the learner can
*see* repeating — the point isn't the icon, it's that by module four they
should be able to guess a new module's shape from the icon before reading a
word of it.

## Code ↔ plain-English blocks

- Code snippet is an exact, unmodified excerpt from the real file, with a visible
  file path + line numbers so the learner can find it themselves.
- Plain-English translation sits beside it, written at the level the learner's
  stated background calls for (see `personalization.md`) — don't explain syntax a
  self-identified-experienced learner already knows; do explain it for someone who
  said they're new to the language.
- Where useful, loosely align specific lines of code to specific sentences of
  explanation (a thin connecting rule or matched background tint is enough — don't
  over-engineer exact line-to-line mapping where the explanation reasonably spans
  several lines).
- The file path above each snippet links to that exact file and line range on
  the source host (GitHub blob URL with a line anchor, when the repo has a
  remote) — one click from "what does this mean" to "show me the real file,"
  not just a label.

## Glossary tooltips

One definition per term, written once, referenced via a shared glossary object:

```js
const glossary = {
  "middleware": "A function that runs on every request before it reaches your route handler — like a checkpoint every request passes through.",
  // ...
};
```

Every occurrence of a glossary term in body text gets the hover/tap treatment; don't
redefine a term inline in prose once it's in the glossary — link to the glossary
behavior instead, so the explanation is maintained in one place.

## Branch switcher (new)

A persistent small control (not a full settings panel) in the top bar: Debug /
Extend / Orient. Switching:
- Jumps to that path's starting module.
- Shared modules referenced by more than one path render once; the switcher just
  changes which module sequence is "active" / highlighted in the progress bar —
  don't duplicate a shared module's HTML per path.
- Switching paths never loses the learner's progress on the path they're leaving —
  it's just a different lens on the same material, not a reset.
