# Design system

One self-contained HTML file. Inline `<style>`, inline `<script>`, no external
requests. It works offline and opens with a double-click, no server needed.

## Look

Avoid the default purple-gradient look of generated pages. Choose a palette and
type pairing from the codebase's own domain, the same way metaphors are chosen
(see `metaphor-bank.md`). A writing tool suits warm paper and ink. A racing or
telemetry app suits something closer to a cockpit dashboard. A media site suits
a muted, editorial look. Commit to one direction per walkthrough.

- Define every color, spacing unit, and type size as a CSS custom property once
  at `:root`, so the whole page can be re-themed from one block.
- Support light and dark mode through `prefers-color-scheme`.
- Leave generous whitespace. Dense code blocks need room around them.
- Use one accent color, sparingly and consistently: the active nav item, the
  progress bar, correct predictions, Observed badges. Modules do not get their
  own accents.
- No emoji. Use inline SVG for icons.

## Layout

- **Sticky top bar** with the walkthrough title, the path switcher (Debug,
  Extend, Orient), and a progress indicator.
- **Assumptions line** immediately below the top bar, stating the expertise level,
  goal, and time budget with a note on how to rebuild.
- **Scroll modules**, one concept each. Let the content set the height, and do not
  put several concepts on one screen.
  - Give each module an anchor (`id="module-slug"`) for deep links and for
    diff-mode addenda to link back to.
  - Arrow keys and space move between modules as well as scrolling.
  - Each module title has a **shape icon** (inline SVG) and a **provenance
    badge** (Observed or Read).
- **Learning loop blocks within each module:**
  1. Frame sentence
  2. Prediction card with confidence control
  3. Reveal block (hidden until commit)
  4. Code and English side by side
  5. Apply card (where applicable)
  6. Go deeper (collapsed, at `new`/`vibe`/`learner` levels)
- **Code and English side by side.** Two columns on wide screens, stacked on
  narrow ones. Real code goes left or top: an exact copy from the repo,
  highlighted with a small embedded highlighter or hand-written token colors,
  never modified. The plain English goes right or below, loosely matched line to
  line.
- **Glossary terms** use a `<dfn>` or `<span class="gloss">` with a custom
  tooltip, because the native `title` tooltip is slow and ugly. The tooltip shows
  a one-line definition on hover or tap. Definitions come from one glossary
  object, so each is written once.

## Provenance badge

Two styles, both small pills next to the module title:

- **Observed**: accent-color background, white text, tooltip "Replayed from a
  real run on {date} at {commit}."
- **Read**: transparent background, muted border, muted text, tooltip "Explained
  from the code. Not run."

Both must be legible in light and dark mode.

## Prediction and apply cards

- Background: a subtle tint that distinguishes the card from the surrounding
  module. Not the accent color.
- Options: buttons with a border, no background until selected. Selected option
  gets the accent color border.
- Confidence control: three small pill buttons below the options. Selected pill
  gets a filled background.
- Commit button: accent color, disabled until both an option and a confidence
  level are selected.
- Reveal: slides in below the card after commit. Correct shows a single
  check mark (inline SVG, not emoji). Wrong shows the actual answer in plain
  text.
- Apply cards use the same style but with a different header ("Apply").

## Plan and brief

- The plan text area has a monospace font and a muted border.
- The "Show the reference plan" button is styled like the commit button.
- Had-it / partly / missed-it marks are inline radio groups next to each step.
- The agent brief block has a dark background (code-block style) with a Copy
  button in the top right corner.

## Motion

- Animation shows a mechanism. A data-flow animation should show something moving
  through real steps, with each beat held long enough to read (at least 600ms).
  When the module is Observed, the animation reads its frames from the trace data.
  - Prefer CSS animations and transitions plus a little vanilla JS over animation
    libraries, to keep the file free of dependencies.
  - Respect `prefers-reduced-motion` by showing a static version, the same
    diagram in its end state.
- Component conversations, such as two services talking, render as a chat
  exchange with alternating bubbles. Each bubble ties to the real function call
  it represents. No invented dialogue.

## Technical limits

- One HTML file. Structured data, such as the narration sync map, the trace data,
  or the progress state, goes in `<script type="application/json">` blocks, not
  separate files.
- No CDN scripts and no web fonts fetched over the network. Use system font
  stacks, or embed a subset of a font only if there is no alternative.
- Keep the file small. Use simple SVG or CSS for animations and images, not video
  or large rasters.
