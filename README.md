# Fieldguide

**Turn any codebase into a personal, interactive course — in one HTML file.**

Point it at a repo. Tell it what you're trying to do. Get back a single self-contained page that teaches you how the code actually works — with scroll-driven animations, branching learning paths, code-to-plain-English translations, and quizzes that test whether you *get it*, not whether you memorized it.

No dependencies. No build step. Works offline. Double-click to open.

---

## Why this exists

You built something with an AI coding agent. It works. But you don't know *how* it works — and the next time it breaks, you're stuck in a loop asking the same agent to fix what it broke.

Or you inherited a codebase. The README says "just run `npm start`." You can run it. You can't reason about it.

Fieldguide closes that gap. It reads the code, asks what you're trying to accomplish, and builds you a course that teaches exactly enough to make you dangerous — not a CS degree, not a full codebase tour, just what you need for what you came to do.

---

## What makes it different

### It asks before it teaches
Most code explainers dump a wall of text at a generic audience. Fieldguide starts with four questions — your goal, what you already know, how much time you have, whether you want narration — and everything it builds is shaped by the answers. A debugger sees different modules than someone just trying to understand the architecture.

### It updates instead of rebuilding
Come back after the code changes and Fieldguide diffs the repo against your last course. Small change? You get a short "what changed and why it matters to you" addendum. Structural rewrite? Full rebuild, with an explanation of why. Nothing changed? It tells you your course is still current and stops.

### Its metaphors aren't random
Every concept in a codebase has a *shape* — gate, pipeline, ledger, cache, queue, boundary, broadcast, lookup, scheduler. Fieldguide classifies the shape first, then picks a metaphor from the codebase's own world. A news-feed aggregator gets wire-service metaphors. A kitchen-management app gets prep-station metaphors. And the system enforces no repeats — you'll never see "think of it like a bouncer" three times in one course.

### It branches by intent
Three paths through every course: **Debug** (trace a failure), **Extend** (add a feature), **Orient** (understand the system). Shared concepts render once; switching paths doesn't reset your progress.

### It can narrate itself
Opt in, and Fieldguide writes a script synced to scroll position — written for the ear, not copy-pasted from the page. Short sentences, contractions, "see that function highlighted above" cues. The deliverable is the script and sync map, ready for any TTS engine.

### Animations that teach, not decorate
Three patterns — data-flow traces, component conversations, architecture build-ups — triggered by scroll, not by a timer you'll never catch. Every animation is replayable, skippable, and respects `prefers-reduced-motion`.

---

## Quick start

```bash
# Copy the skill folder into your Claude Code skills directory
cp -r fieldguide/ ~/.claude/skills/

# Open any project and say:
# "Turn this into a course"
# "Make me a fieldguide for this"
# "Teach me how this code works"
# "Update my fieldguide"  (triggers diff mode)
```

---

## What it produces

A single `.course.html` file and a `.course.json` sidecar (for diff mode). The HTML is fully self-contained — inline CSS, inline JS, no network requests, no CDN fonts. Open it in any browser, on any device, online or off.

**Inside the HTML:**
- Scroll-based modules with progress tracking and keyboard navigation
- Code snippets that are exact copies from the repo, linked to their real file and line on GitHub
- Side-by-side code ↔ plain-English translations calibrated to your stated experience level
- Animated visualizations (data flow, component conversations, architecture build-ups)
- Quizzes that test application — with real second-chance questions on wrong answers, not just answer keys
- Glossary tooltips, one definition per term, maintained in one place
- A persistent branch switcher (Debug / Extend / Orient) in the top bar
- Shape icons per module showing the underlying pattern — by module four, you start recognizing the shapes before reading a word
- A domain-matched visual identity (not the default gradient-and-sans-serif AI look)
- Light and dark mode via `prefers-color-scheme`
- An explicit note at the end saying what was *left out* and why — selective, not incomplete

---

## How it works under the hood

Fieldguide is a Claude Code skill — a folder of structured instructions that guide an AI agent through a specific kind of generation task. It's not a template engine; it's a methodology.

```
fieldguide/
├── SKILL.md                              # The generation flow
├── examples/
│   └── follow-builders.course.html       # A real fieldguide, built against
│                                          # zarazhangrui/follow-builders
└── references/
    ├── personalization.md                 # Intake questions & defaults
    ├── diff-mode.md                       # Course state schema & change classification
    ├── metaphor-bank.md                   # Shape taxonomy & domain-flavor guidance
    ├── narration.md                       # Script style & sync map format
    ├── design-system.md                   # Visual direction & layout rules
    └── interactive-elements.md            # Quizzes, animations, glossary, branching
```

The generation flow:
1. **Intake** — ask the learner who they are and what they need
2. **Diff check** — if a previous course exists, classify the change
3. **Map** — trace one real user action end-to-end through the codebase
4. **Branch** — route into Debug / Extend / Orient
5. **Classify & draw metaphors** — shape first, surface metaphor second
6. **Build** — write the single HTML file
7. **Narrate** (optional) — write the audio script and sync map
8. **Save state** — write the JSON sidecar for next time

---

## Credit where it's due

The core idea — turning a codebase into a single-file interactive HTML course with scroll-based modules, code-to-English translations, animated visualizations, and application-testing quizzes — comes from [codebase-to-course](https://github.com/zarazhangrui/codebase-to-course) by [Zara Zhang](https://x.com/zarazhangrui). That project's design philosophy ("build first, understand later," "show don't tell," "no recycled metaphors," "original code only") is preserved here.

Fieldguide is not a fork — it's a reimplementation with five additions built on top of that foundation: personalized intake, diff mode, a structured metaphor bank, opt-in narration, and branching paths. The attribution is explicit because the idea deserves it.

---

## License

MIT
