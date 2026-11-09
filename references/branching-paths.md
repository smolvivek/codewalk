# Branching paths

Every walkthrough has three paths: **Debug**, **Extend**, and **Orient**. The
switcher UI is described in `interactive-elements.md`. This file says what each
path teaches differently: which concepts, in what order, how deep, and in what
tone.

All three paths draw on the same concept map (see `codebase-mapping.md`). They
differ in which concepts come first, which sit in the background, and what the
reader should be able to do at the end.

## Orient

**The reader's question:** How does this thing work?

**Goal:** The reader can explain the architecture to someone else in plain
language and can predict roughly where a given behavior lives in the code.

**Concepts:**

- Include every concept the trace touches. This is the broadest path.
- Weight toward Boundary, Pipeline, and Broadcast shapes. They are the structure
  a newcomer needs first.
- Give Gates and Ledgers shorter treatment unless they are central to the design.

**Order:** Big picture, then zoom in. Open with the highest-level shape, usually
a Boundary or Pipeline that shows the whole flow. Then walk through the concepts
in the order that builds understanding, which may differ from execution order.
End with the concept that ties the rest together.

**Depth:** Even. No concept gets much more space than another. The reader is
building a map and is not going deep on any one part.

**Tone:** Tour guide. "Here is what this does and why it is here." Explain what
the reader is looking at. Do not tell them what to change.

**Predictions:** "Given what you now know, where would you expect to find X?"
They test the mental map, not a specific mechanism. At `vibe` level, frame
predictions in terms of the app's behavior. At `engineer` level, ask about
design decisions.

**Apply:** "If a user does Y, which module handles it?" Tests whether the reader
can navigate the map.

**Done means:** The reader can sketch a rough box diagram of the system from
memory and label each box correctly. In the plan-then-brief closing, the plan
asks what they would change or ask their agent to build next.

---

## Debug

**The reader's question:** Something is broken and I need to find and fix it.

**Goal:** The reader can trace a failure from symptom to root cause in this
codebase and understands the mechanisms well enough to describe the fix, even if
an AI agent will write it.

**Concepts:**

- Start from the symptom if one was given, or from the most failure-prone part of
  the trace. If the reader said "the API returns 500 on this endpoint," start
  there.
- **Foreground** Gates (validation and auth, where things get rejected), Ledgers
  (state that can go stale or corrupt), and Boundaries (where mismatches between
  systems cause failures).
- **Background** Pipelines and Broadcasts. They explain how things flow when they
  work, and a debugger needs to know where they break.
- Cut concepts that are unlikely failure points unless they sit on the direct path
  from symptom to cause.

**Order:** Symptom to cause. Module one says what goes wrong. Module two says
what the code does at that point. Each later module moves one step closer to the
root. The last module covers the mechanism that is broken, or most likely broken
if the reader has not given the exact bug.

**Depth:** Uneven on purpose. Concepts on the failure path get the full
treatment: the learning loop with predictions about what each step produces.
Supporting concepts get just enough to follow the trace.

**Tone:** Investigator. "Let's trace this." Direct, with no detours. Every module
is one step on the trail from symptom to cause.

**Predictions:** "This function receives X. Given the code you just saw, what
does it return?" They test whether the reader can run the code in their head,
which is what debugging requires.

**Apply and Break it:** Debug path modules include Break it questions where a
failure teaches the mechanism better than a success. "What happens if this check
is removed?" See `learning-loop.md` for Break it rules. Apply questions ask the
reader to locate or describe a fix.

**Done means:** The reader can describe the most likely failure path and where to
intervene, in enough detail to instruct an AI coding agent to fix it without a
guessing loop. The plan-then-brief closing produces a bug-fix brief.

---

## Extend

**The reader's question:** I want to add or change something. Where does it go?

**Goal:** The reader understands the existing pattern well enough to know where
new code belongs, what it plugs into, and what it should leave alone. That is
enough to spec the change for an AI agent or write it themselves.

**Concepts:**

- Find the existing feature nearest to what the reader wants to add. Its full
  trace is the core of the walkthrough.
- **Foreground** the mechanism the reader will extend or imitate. Whatever shape
  it is, it gets the deepest treatment, because the reader needs to be able to
  copy or modify the pattern.
- **Also foreground** the boundaries the new code will cross and any Gate it must
  pass through, such as validation, auth, or permissions.
- **Background** everything the new feature does not touch. One-line mentions,
  not modules.
- **Always include** the registration step: wherever new features hook in,
  whether that is a route table, a plugin manifest, a switch statement, or an
  event listener. The reader needs to know where to plug in, not only what to
  write.

**Order:** Existing pattern, then where to intervene. Module one shows the
feature the reader will imitate or extend, fully traced. Then cover what it
connects to, where it registers, and what constraints it works under. The last
module is a concrete pointer to where the new code goes.

**Depth:** Deep on the pattern being extended and shallow on everything else.

**Tone:** Mentor. "Here is how the existing one works. Here is where yours would
go. Here is what to watch for." Practical and forward-looking. Anticipate the
reader's next step instead of only describing what exists.

**Predictions:** "You want to add feature Y. Based on the pattern you just saw,
which file would you create or change first?" They test whether the reader can
apply the pattern, not just recognize it. At `vibe` level, frame it as what to
tell the agent.

**Apply:** "Your agent says it added a new route but skipped the auth middleware.
What do you check?" Tests whether the reader can verify the agent's work.

**Done means:** The reader can write a 3 to 5 step plan for their change that an
AI coding agent could follow without inventing an architecture. The plan-then-
brief closing produces exactly this.

---

## Shared modules

Some concepts appear in two or all three paths. Do not duplicate them. Render the
module once in the HTML and include it in each path that uses it. The switcher
controls which modules are active, and a shared module's HTML exists once.

When a concept appears in several paths at different depths:

- Write it at the deepest level any path needs.
- The shallower paths can use the same module. Extra depth does not hurt an
  Orient reader, and cutting detail would hurt an Extend reader.
- Exception: if Debug needs a different framing of the same concept (symptom
  first versus explanation first), write two modules and assign one to each path.
  Do not make one shared module serve two incompatible purposes.

## Default path

If intake did not produce a clear goal, use Orient. It is the safest choice,
since a reader who only said "explain this" gets a full map. Switching to Debug
or Extend later is a narrowing, which is easier than broadening.

## Switching paths

See `interactive-elements.md` for the UI. The content rules are:

- Switching never resets progress. If the reader finished 4 of 6 modules on
  Orient and switches to Debug, any module shared by both stays marked read, and
  the progress bar recalculates for the new path's module count.
- The first module of each path must work as a starting point even if the reader
  has already read other modules. Put a short note at the top, such as "You are
  now in Debug mode. Here is what we are looking for." Do not recap what they
  have already seen.
