# Interactive elements

## Prediction cards

Every module has a prediction card as its first interactive element, after the
frame sentence. See `learning-loop.md` for the full rules.

### Markup

```html
<div class="predict-card" data-concept="auth-gate" data-correct="b">
  <p class="predict-question">A user hits this endpoint without a token.
  What happens?</p>
  <div class="predict-options">
    <button data-option="a">The request reaches the handler and returns empty data</button>
    <button data-option="b">The middleware rejects it before the handler runs</button>
    <button data-option="c">The server crashes with an unhandled error</button>
    <button data-option="d" data-skip="true">I don't know</button>
  </div>
  <div class="confidence-control">
    <span>How sure?</span>
    <button data-confidence="guessing">Guessing</button>
    <button data-confidence="think-so">Think so</button>
    <button data-confidence="sure">Sure</button>
  </div>
  <button class="commit-btn" disabled>Lock in</button>
</div>
```

The commit button enables only when both an option and a confidence level are
selected. Once committed, the choice and confidence are locked and the reveal
section appears.

### Reveal

After the reader commits, show a reveal block:

```html
<div class="reveal-block" hidden>
  <p class="reveal-result"><!-- "That matched." or "The actual answer: ..." --></p>
  <div class="reveal-detail"><!-- The code, the trace value, or both --></div>
</div>
```

A wrong guess is not scolded. Say what actually happens. If the module is
Observed, the replay shows the recorded run. If it is Read, say so.

### Apply card

Same structure as the prediction card but with `class="apply-card"`. Uses a new
situation, not the same example. A wrong answer triggers one simpler follow-up
before the module moves on.

## Provenance badge

Every module title has a badge showing its provenance:

```html
<span class="provenance-badge" data-provenance="observed"
  title="Replayed from a real run on 2026-11-09 at commit 7ff0522">
  Observed
</span>
```

Or `data-provenance="read"` with title "Explained from the code. Not run."

Style the badge as a small pill next to the module title. Observed gets the
accent color background. Read gets a muted outline. Both are visible in light
and dark mode.

## Animated visualizations

There are three patterns. Use more than one in a walkthrough, because repeating
one pattern is the animation version of a recycled metaphor.

1. **Data flow.** An element (a dot, a packet, a request) moves through labeled
   stages and pauses at each with a one-line caption. When the module is Observed,
   the dot carries the recorded payload from the trace. Suits pipelines,
   middleware chains, and request lifecycles.
2. **Component conversation.** A chat-style exchange between two or more named
   components. Each bubble shows, on tap or hover, the actual line of code it
   stands for. Suits request and response, pub/sub, and API calls between
   services.
3. **Architecture build-up.** A diagram that assembles itself piece by piece as the
   module text progresses, linked to scroll or to steps, instead of appearing all
   at once. Suits modules about how the pieces fit together.

**Trigger on scroll, not on load.** Attach every animation to an
IntersectionObserver on its own module. A timer that starts at page load means a
module three screens down plays before anyone sees it. Each animation plays once
when its module scrolls into view. It must be replayable through a small restart
control, and skippable to its end state.

## Shape icons

Each module has a small inline SVG icon next to its title for the shape it
teaches: gate, ledger, pipeline, queue, cache, broadcast, lookup, boundary, or
scheduler (see `metaphor-bank.md`). The icon makes the no-repeat rule visible.
By the fourth module the reader should be able to guess a new module's shape from
the icon before reading any of it.

## Code and English blocks

- The code is an exact, unmodified excerpt from the real file, with the file path
  and line numbers shown so the reader can find it.
- The plain English sits beside it, pitched at the reader's expertise level (see
  `expertise-levels.md`). At `new` and `vibe`, behavior before syntax. At
  `engineer`, skip definitions and lead with design decisions.
- Where it helps, line up specific lines of code with specific sentences using a
  thin connecting rule or a matching background tint. Exact line-for-line mapping
  is not needed when one explanation reasonably covers several lines.
- The file path above each snippet links to that file and line range on the source
  host (a GitHub blob URL with a line anchor, when the repo has a remote). The
  reader is one click from the explanation to the real file.

## Go deeper blocks

At `new`, `vibe`, and `learner` levels, each module has one collapsed block:

```html
<details class="go-deeper">
  <summary>Go deeper</summary>
  <!-- Content written for the next level up -->
</details>
```

It is optional and never needed to follow the main text. At `engineer` level,
omit it.

## Glossary tooltips

Write each definition once, in a shared object:

```js
const glossary = {
  "middleware": "A function that runs on every request before it reaches your route handler.",
  // ...
};
```

Every occurrence of a glossary term in body text gets the hover or tap tooltip.
Once a term is in the glossary, do not redefine it inline. That keeps each
explanation in one place.

## Branch switcher

A small persistent control in the top bar, not a settings panel: Debug, Extend,
Orient. Switching does three things:

- It jumps to the start of that path.
- Modules shared between paths render once. The switcher changes which sequence is
  active in the progress bar. It does not duplicate the module's HTML.
- It keeps the reader's progress on the path they left. It changes the view of the
  same material and does not reset anything.

## Plan and brief blocks

The closing module has three parts. See `agent-brief.md` for full rules.

1. A text area for the reader's plan, saved to localStorage.
2. A "Show the reference plan" button that reveals the reference plan with
   had-it / partly / missed-it marks per step.
3. A copyable agent brief block assembled from the concept map and the reader's
   progress.

## Progress persistence

On each prediction or apply answer, write the full progress object to both
localStorage (key: `codewalk-progress-{repo-name}`) and the embedded
`#quiz-state` block:

```json
{
  "level": "vibe",
  "concepts": {
    "auth-gate": {"prediction": "right", "apply": "passed", "confidence": "sure"},
    "dedup-ledger": {"prediction": "wrong", "apply": "missed", "confidence": "sure"}
  },
  "plan": {
    "text": "",
    "reference_marks": {}
  }
}
```

Wrap all localStorage access in try/catch, for private browsing and full storage.
On load, restore progress from localStorage when available, so a returning reader
sees which modules they finished.

The footer "Copy my progress" button serializes the full progress object as
formatted JSON and calls `navigator.clipboard.writeText`.
