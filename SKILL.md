---
name: fieldguide
description: Turn any codebase into a personal, branching, narrated interactive HTML course. Use when the user says "turn this into a course," "explain this codebase interactively," "teach me how this code works," "make me a fieldguide for this," or similar.
---

# Fieldguide

Point this skill at a codebase. It produces a single self-contained HTML file that
teaches a specific learner, with a specific goal, how the code actually works — by
tracing what happens when the app is used, not by lecturing at them.

Every codebase has a shape before it has a syntax. A fieldguide teaches the shape
first — what's a gate, what's a ledger, what's a pipeline — then lets the syntax
hang off something the learner can already picture, in terms drawn from the
codebase's own world, not a generic default.

This builds on the idea and design philosophy of
[codebase-to-course](https://github.com/zarazhangrui/codebase-to-course) by
[Zara Zhang](https://x.com/zarazhangrui) — scroll-based modules, code-to-plain-English
translation, "build first, understand later," and "quizzes test doing, not knowing"
are hers, reimplemented here with credit. Five things are added on top: it asks who
it's for before it builds, it can update instead of rebuild, its metaphors come from
a structured system instead of being invented ad hoc each time, it can narrate
itself, and it branches by what the learner is actually there to do.

## Who this is for

"Vibe coders" — people who build or inherit software by instructing AI coding tools
in natural language, without a traditional CS education. They've got something
working but don't know *how* it works under the hood, and they're not trying to
become software engineers. They want coding as a superpower: steer AI tools better,
catch hallucinated or bad code, break out of bug loops, talk to engineers without
feeling lost.

## Overall flow

1. **Intake** — ask the learner who they are and what they're here for (see
   `references/personalization.md`). Skip only if the request already answered it.
2. **Check for a previous fieldguide** — if one exists for this repo (a
   `*.course.json` sidecar), offer diff mode instead of a full rebuild (see
   `references/diff-mode.md`).
3. **Map the codebase** — find the entry point, trace one real user action
   end-to-end, identify the 5-9 concepts that action touches. Cover what the
   learner's stated goal needs, not everything that exists.
4. **Pick the branch** — route into Debug / Extend / Orient.
5. **Classify and draw metaphors** — for each concept, classify its shape first,
   then pull or mint a metaphor from the bank (see `references/metaphor-bank.md`).
   Never reuse a metaphor within one fieldguide.
6. **Write it** — build the single HTML file per `references/design-system.md` and
   `references/interactive-elements.md`. Use more than one animation pattern.
7. **Optionally script narration** — if opted in, write it per `references/narration.md`.
8. **Save course state**, including quiz results format, for next time.
9. **Hand it back** — where the file is, roughly how long it takes. The fieldguide
   speaks for itself; don't narrate what's inside it.

## What it keeps from the original

Single HTML file. No dependencies, no build step, works offline.

- Scroll-based modules, progress tracking, keyboard navigation.
- Code ↔ plain-English translations — real, unmodified code next to its meaning.
- Animated visualizations tracing real mechanism, not decoration.
- Quizzes that test application, never recall.
- Glossary tooltips, one definition per term.
- A distinctive visual identity drawn from the codebase's own domain — never the
  default purple-gradient AI look.

## What's added

1. **Personalization** — intake before generation. Goal, known stack, and time
   budget each reshape what gets built, not just how it's worded.
2. **Diff mode** — a returning learner gets a short "what changed and why"
   addendum, not a full regenerate, and missed quiz concepts get re-tested even
   when the underlying code didn't change.
3. **A structured metaphor bank** — metaphors classified by shape (gate, ledger,
   pipeline, queue, cache, broadcast, lookup, boundary, scheduler) before a
   surface metaphor is picked, so "never repeat a metaphor" is an enforced system
   and the shape itself becomes something the learner starts recognizing across
   codebases, not just within one.
4. **Narration** — opt-in script written for the ear, synced to scroll position.
5. **Branching paths** — Debug / Extend / Orient, so the course teaches toward
   what the learner came to do, not a fixed tour.

## How to use

Copy this folder into `~/.claude/skills/`, open a project, and say any of:

- "Turn this into a course"
- "Make me a fieldguide for this"
- "Explain this codebase interactively"
- "Teach me how this code works"
- "Update my fieldguide" (triggers diff mode)

## Design philosophy

**Build first, understand later.** Build something → experience it working → now
understand how it works.

**Show, don't tell.** Every screen at least 50% visual. If it can be a diagram,
animation, or interactive element, it shouldn't be a paragraph.

**Quizzes test doing, not knowing**, with a real second attempt on a wrong answer,
not just an answer key.

**No recycled metaphors** — enforced by shape classification, not just a rule.

**Original code only.** Snippets are exact copies, linked to the real file and line.

**Teach to the goal, not the map.** A fieldguide is not obligated to explain the
whole codebase — it's obligated to make the learner capable of what they came to
do. Say what was cut and why, so it reads as selective, not incomplete.

## Structure

```
fieldguide/
├── SKILL.md
├── examples/
│   └── follow-builders.course.html   # a real fieldguide, generated against
│                                       # zarazhangrui/follow-builders
└── references/
    ├── design-system.md
    ├── interactive-elements.md
    ├── metaphor-bank.md
    ├── personalization.md
    ├── diff-mode.md
    └── narration.md
```
