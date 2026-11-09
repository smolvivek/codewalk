# Design system

A single self-contained HTML file. Inline `<style>`, inline `<script>`, no external
requests, works offline, works from a double-click with no server.

## Look and feel

Not the default purple-gradient AI-generated look. Pick a palette and type pairing
that fits the *codebase's own domain* the same way metaphors do (see
`metaphor-bank.md`) — a warm, paper-and-ink palette for a writing tool; something
closer to a dashboard/cockpit for a racing or telemetry app; muted and editorial for
a media site. Commit to one distinctive direction per course rather than a safe
generic theme.

- CSS custom properties for every color, spacing unit, and type size, defined once
  at `:root` — makes the whole course re-themeable from one block if regenerated.
- Support both light and shipped-dark via `prefers-color-scheme`, same as any other
  artifact in this ecosystem.
- Generous whitespace. Dense code blocks need visual room around them, not next to
  them.
- One accent color used sparingly and consistently — for the active nav item, the
  progress bar, correct-quiz-answer states. Don't let every module pick its own
  accent.

## Layout

- **Sticky top bar**: course title, path switcher (Debug / Extend / Orient — see
  SKILL.md), progress indicator.
- **Scroll-based modules**, one concept each, full viewport height is fine but don't
  force it — let content set the height, just don't cram multiple concepts into one
  screen.
  - Section anchors (`id="module-slug"`) for deep linking and for the diff-mode
    addendum to link back into.
  - Keyboard nav: arrow keys / space move between modules, not just scroll.
- **Code ↔ plain-English**: two-column on wide viewports, stacked on narrow ones —
  real code left/top (exact copy from the repo, syntax-highlighted with a small
  embedded highlighter or hand-rolled token coloring, never modified or simplified),
  plain English right/bottom, loosely line-matched.
- **Glossary terms**: a `<dfn>` or `<span class="gloss">` with a `title`-less custom
  tooltip (native `title` is too slow/ugly) that shows a one-line definition on
  hover/tap, sourced from a single glossary object built once and referenced
  everywhere a term recurs, so the definition is written once per term.

## Motion

- Animations illustrate mechanism, not decoration — a data flow animation should
  show something actually moving through actual steps, timed to be readable (nothing
  under ~600ms per beat), not a flashy flourish.
  - Prefer CSS animations / transitions and small amounts of vanilla JS over heavy
    animation libraries, to keep the file dependency-free.
  - Respect `prefers-reduced-motion`: provide a static equivalent (the same diagram,
    end-state only) rather than forcing motion on everyone.
- Component "conversations" (e.g. two services talking) render as a chat-style
  exchange — alternating bubbles, each one tied to the real function call it
  represents, not an invented dialogue.

## Technical constraints

- One HTML file. If narration sync or course state needs structured data, embed it
  as `<script type="application/json">` blocks rather than separate files.
- No CDN scripts, no web fonts fetched over the network — the whole point is it
  works offline. Pick system font stacks or embed a font as a subset if absolutely
  necessary (prefer not to).
- Keep total file size reasonable — large embedded animations/images should be
  simple SVG or CSS, not embedded video or large rasters.
