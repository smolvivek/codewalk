# Interactive elements

## Quizzes

Test application, never recall.

- Bad: "What does API stand for?"
- Good: "A user reports stale data after switching pages. Based on the cache module
  you just read, where would you look first?"

A question should be answerable only by someone who understood the mechanism, not by
someone who remembered a term from the paragraph above it. Multiple choice is fine.
Include at least one wrong answer that reflects a common, real misunderstanding of the
mechanism. No joke answers.

Give feedback right away, in one line that says why, tied to the code or diagram the
module just showed. "Correct" and "try again" are not feedback.

A wrong answer should not just reveal the right one. Follow it with one simpler, more
concrete question that isolates the misunderstanding the wrong choice implied. That
gives the reader a real second attempt before moving on.

## Animated visualizations

There are three patterns. Use more than one in a walkthrough, because repeating one
pattern is the animation version of a recycled metaphor.

1. **Data flow.** An element (a dot, a packet, a request) moves through labeled stages
   and pauses at each with a one-line caption. Suits pipelines, middleware chains, and
   request lifecycles.
2. **Component conversation.** A chat-style exchange between two or more named
   components. Each bubble shows, on tap or hover, the actual line of code it stands
   for. Suits request and response, pub/sub, and API calls between services.
3. **Architecture build-up.** A diagram that assembles itself piece by piece as the
   module text progresses, linked to scroll or to steps, instead of appearing all at
   once. Suits modules about how the pieces fit together.

**Trigger on scroll, not on load.** Attach every animation to an IntersectionObserver
on its own module. A timer that starts at page load means a module three screens down
plays before anyone sees it. Each animation plays once when its module scrolls into
view. It must be replayable through a small restart control, and skippable to its end
state.

## Shape icons

Each module has a small inline SVG icon next to its title for the shape it teaches:
gate, ledger, pipeline, queue, cache, broadcast, lookup, boundary, or scheduler (see
`metaphor-bank.md`). The icon makes the no-repeat rule visible. By the fourth module
the reader should be able to guess a new module's shape from the icon before reading
any of it.

## Code and English blocks

- The code is an exact, unmodified excerpt from the real file, with the file path and
  line numbers shown so the reader can find it.
- The plain English sits beside it, pitched at the background the reader gave at
  intake (see `personalization.md`). Do not explain syntax to an experienced reader.
  Do explain it to someone who said they are new to the language.
- Where it helps, line up specific lines of code with specific sentences using a thin
  connecting rule or a matching background tint. Exact line-for-line mapping is not
  needed when one explanation reasonably covers several lines.
- The file path above each snippet links to that file and line range on the source
  host (a GitHub blob URL with a line anchor, when the repo has a remote). The reader
  is one click from the explanation to the real file.

## Glossary tooltips

Write each definition once, in a shared object:

```js
const glossary = {
  "middleware": "A function that runs on every request before it reaches your route handler, like a checkpoint every request passes through.",
  // ...
};
```

Every occurrence of a glossary term in body text gets the hover or tap tooltip. Once a
term is in the glossary, do not redefine it inline. That keeps each explanation in one
place.

## Branch switcher

A small persistent control in the top bar, not a settings panel: Debug, Extend,
Orient. Switching does three things:

- It jumps to the start of that path.
- Modules shared between paths render once. The switcher changes which sequence is
  active in the progress bar. It does not duplicate the module's HTML.
- It keeps the reader's progress on the path they left. It changes the view of the
  same material and does not reset anything.
