# Design system

One self-contained HTML file. Inline `<style>`, inline `<script>`, no external
requests. It works offline and opens with a double-click, no server needed.

## Look

Avoid the default purple-gradient look of generated pages. Choose a palette and type
pairing from the codebase's own domain, the same way metaphors are chosen (see
`metaphor-bank.md`). A writing tool suits warm paper and ink. A racing or telemetry
app suits something closer to a cockpit dashboard. A media site suits a muted,
editorial look. Commit to one direction per walkthrough.

- Define every color, spacing unit, and type size as a CSS custom property once at
  `:root`, so the whole page can be re-themed from one block.
- Support light and dark mode through `prefers-color-scheme`.
- Leave generous whitespace. Dense code blocks need room around them.
- Use one accent color, sparingly and consistently: the active nav item, the progress
  bar, correct quiz answers. Modules do not get their own accents.
- No emoji. Use inline SVG for icons.

## Layout

- **Sticky top bar** with the walkthrough title, the path switcher (Debug, Extend,
  Orient), and a progress indicator.
- **Scroll modules**, one concept each. Let the content set the height, and do not put
  several concepts on one screen.
  - Give each module an anchor (`id="module-slug"`) for deep links and for diff-mode
    addenda to link back to.
  - Arrow keys and space move between modules as well as scrolling.
- **Code and English side by side.** Two columns on wide screens, stacked on narrow
  ones. Real code goes left or top: an exact copy from the repo, highlighted with a
  small embedded highlighter or hand-written token colors, never modified. The plain
  English goes right or below, loosely matched line to line.
- **Glossary terms** use a `<dfn>` or `<span class="gloss">` with a custom tooltip,
  because the native `title` tooltip is slow and ugly. The tooltip shows a one-line
  definition on hover or tap. Definitions come from one glossary object, so each is
  written once.

## Motion

- Animation shows a mechanism. A data-flow animation should show something moving
  through real steps, with each beat held long enough to read (at least 600ms).
  - Prefer CSS animations and transitions plus a little vanilla JS over animation
    libraries, to keep the file free of dependencies.
  - Respect `prefers-reduced-motion` by showing a static version, the same diagram in
    its end state.
- Component conversations, such as two services talking, render as a chat exchange
  with alternating bubbles. Each bubble ties to the real function call it represents.
  No invented dialogue.

## Technical limits

- One HTML file. Structured data, such as the narration sync map or the quiz state,
  goes in `<script type="application/json">` blocks, not separate files.
- No CDN scripts and no web fonts fetched over the network. Use system font stacks,
  or embed a subset of a font only if there is no alternative.
- Keep the file small. Use simple SVG or CSS for animations and images, not video or
  large rasters.
