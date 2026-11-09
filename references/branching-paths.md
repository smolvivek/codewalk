# Branching paths

Three paths through every course: **Debug**, **Extend**, **Orient**. The branch
switcher UI is in `interactive-elements.md`. This file specifies what each path
*teaches differently* — concept selection, ordering, depth, and tone.

All three paths draw from the same concept map (see `codebase-mapping.md`). The
difference is which concepts are foregrounded, which are background, and what
the course is trying to make the learner capable of doing when it's done.

## Orient

**The learner's question:** "How does this thing work?"

**Goal:** After this course, the learner can explain the system's architecture to
someone else in plain language, and can predict roughly where a given piece of
behavior lives in the code.

**Concept selection:**
- Include every concept the trace touches. This is the broadest path.
- Weight toward Boundary, Pipeline, and Broadcast shapes — these are the
  structural scaffolding a newcomer needs first.
- Gates and Ledgers get shorter treatment unless they're architecturally central.

**Ordering:** Big picture → zoom in. Start with the highest-level shape (usually
a Boundary or Pipeline that shows the whole system's flow), then walk through
each concept in the order that builds understanding, not necessarily execution
order. End with the concept that ties everything together.

**Depth:** Even. No concept gets dramatically more space than another. The
learner isn't going deep on anything — they're building a mental map.

**Tone:** Tour guide. "Here's what this does and why it's here." Explanatory,
not prescriptive. Don't tell them what to change; tell them what they're looking
at.

**Quiz focus:** "Given what you now know about the system, where would you expect
to find X?" — testing the mental map, not a specific mechanism.

**What "done" means:** The learner can draw a rough box diagram of the system
from memory and label each box correctly.

---

## Debug

**The learner's question:** "Something is broken and I need to find/fix it."

**Goal:** After this course, the learner can trace a failure from symptom to root
cause in this codebase, and understands the mechanisms well enough to describe the
fix (even if they'll use an AI agent to write it).

**Concept selection:**
- Start from the symptom (if stated) or from the most failure-prone part of the
  trace. If the learner said "API returns 500 on this endpoint," start there.
- **Foreground:** Gates (validation, auth — where things get rejected), Ledgers
  (state that can get stale or corrupted), Boundaries (where mismatches between
  systems cause failures).
- **Background:** Pipelines and Broadcasts get shorter treatment — they matter
  for understanding flow, but the debugger needs to know *where things break*,
  not *how things flow when they work*.
- Cut concepts that are unlikely failure points unless they're in the direct
  trace from symptom to cause.

**Ordering:** Symptom → cause. The first module is "here's what goes wrong,"
the second is "here's what the code does at that point," and each subsequent
module traces one step closer to the root. The last module is the mechanism
that's actually broken (or most likely broken, if the learner hasn't specified
the exact bug).

**Depth:** Uneven on purpose. The failure-relevant concepts get full treatment
(metaphor, code walkthrough, visualization, quiz). Supporting concepts get
enough to follow the trace but no more.

**Tone:** Investigator. "Let's trace this." Direct, no wandering. Every module
earns its place by being one step in the trail from symptom to cause.

**Quiz focus:** "This function receives X input. Given the code you just saw,
what would it return? And what would happen downstream?" — testing whether the
learner can mentally execute the code, because that's what debugging requires.

**What "done" means:** The learner can describe the most likely failure path and
where to intervene, in enough detail to instruct an AI coding agent to fix it
without a guessing loop.

---

## Extend

**The learner's question:** "I want to add/change something. Where does it go?"

**Goal:** After this course, the learner understands the existing pattern well
enough to know *where* new code should go, *what* it should plug into, and *what
it shouldn't touch* — enough to spec the change for an AI agent or write it
themselves.

**Concept selection:**
- Identify the nearest existing feature to what the learner wants to add. That
  feature's full trace is the core of the course.
- **Foreground:** The mechanism the learner will be extending or imitating.
  Whatever shape it is, that shape gets the deepest treatment — because the
  learner needs to understand the pattern well enough to replicate or modify it.
- **Also foreground:** Boundaries the new code will cross, and any Gate that
  the new feature needs to pass through (validation, auth, permissions).
- **Background:** Everything else in the system that the new feature doesn't
  touch. One-line mentions, not full modules.
- **Always include:** The config/routing/registration step — wherever new
  features "register" themselves in this codebase (a route table, a plugin
  manifest, a switch/case, an event listener). The learner needs to know where
  to plug in, not just what to write.

**Ordering:** Existing pattern → where to intervene. The first module shows the
feature the learner will be imitating or extending, fully traced. Then: what
it connects to, where it registers, what constraints it operates under. The last
module is a concrete "here's where your new code goes" pointer.

**Depth:** Deep on the pattern being extended, shallow on everything else.

**Tone:** Mentor. "Here's how the existing one works. Here's where yours would
slot in. Here's what to be careful about." Practical, forward-looking. The
course anticipates the learner's next step rather than just describing what
exists.

**Quiz focus:** "You want to add feature Y. Based on the pattern you just saw,
which file would you create/modify first, and what function would you call?" —
testing whether the learner can apply the pattern, not just recognize it.

**What "done" means:** The learner can write a 3-5 step plan for their change
that an AI coding agent could follow without hallucinating the architecture.

---

## Shared modules

Some concepts appear in all three paths (or two of three). Don't duplicate them.
Render the module once in the HTML and include it in all paths that reference it.
The branch switcher controls which modules are visible/active, but a shared
module's HTML exists once.

When a concept appears in multiple paths but at different depths:
- Write it at the **deepest** level any path needs.
- For shallower paths, the same module works — extra depth doesn't hurt an Orient
  learner, and cutting detail for the Extend learner would.
- Exception: if the Debug path needs a fundamentally different framing of the
  same concept (symptom-first vs. explanation-first), write it as two modules
  and assign each to its path. Don't force a shared module to serve two
  incompatible pedagogical purposes.

## Default path

If intake didn't produce a clear goal, default to Orient. It's the safest — a
learner who just said "explain this" gets a full map. From there, switching to
Debug or Extend is a narrowing move, which is easier than broadening.

## Path switcher behavior

See `interactive-elements.md` for the UI spec. Content-side rules:

- Switching paths never resets progress. If the learner read 4/6 modules on
  Orient and switches to Debug, any module shared between the two paths stays
  "read." The progress bar recalculates for the new path's module count.
- The first module of each path should make sense as a starting point even if
  the learner already read other modules — a brief "you're now in Debug mode,
  here's what we're looking for" orientation line at the top, not a recap of
  everything they've already seen.
