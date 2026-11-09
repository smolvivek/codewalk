# Codebase mapping

How to read a codebase you've never seen and decide what to teach. This is the
analytical step between intake (who's the learner, what do they want) and writing
(modules, metaphors, visuals). Get it wrong and the course teaches the wrong things
confidently.

## Find the entry point

Every codebase has at least one place where "a user does something and the code
responds." That's the entry point. Not main(), not index.js — the place where a
real action enters the system.

How to find it, in order of reliability:

1. **README / docs** — most repos say "run this, then visit localhost:3000" or
   "this script does X." That's the action.
2. **Scripts / commands** — `package.json` scripts, Makefile targets, CLI entry
   points, GitHub Actions workflows. These are what the developer actually runs.
3. **Route handlers / API definitions** — if it's a web app, grep for route
   definitions (Express `app.get`, FastAPI `@app.route`, Rails `routes.rb`).
   Pick the most common or most representative one.
4. **Main function / top-level execution** — the fallback. `if __name__ == "__main__"`,
   `func main()`, the top of a script that runs on import.

If the learner said they're debugging something specific, *their bug report is the
entry point* — trace from where the symptom appears, not from where the code starts.

If the learner said they're extending something, the entry point is the nearest
existing feature to what they want to add.

## Trace one action end-to-end

Starting from the entry point, follow exactly one user action through the code.
Not "all the things the app can do" — one action, fully traced.

Read the code in execution order, not file order:
1. Start at the entry point function/handler.
2. For each call it makes, open that function and read it.
3. Note each *conceptually distinct thing* that happens — a check, a
   transformation, a storage operation, a message sent, a response returned.
4. Stop when the action is complete (a response is sent, a file is written,
   a process exits).

Keep a running list:
```
entry: POST /api/digest → handleDigest()
  → loadConfig()           [Lookup — resolves user preferences]
  → fetchSources()         [Boundary — calls external APIs]
  → deduplicateItems()     [Ledger — checks what's been seen before]
  → formatDigest()         [Pipeline — transforms raw items to readable output]
  → deliver()              [Pipeline — sends via configured channel]
```

That list, with shapes attached, is the concept map.

## Select 5-9 concepts

The trace usually surfaces more concepts than a course should cover. Filter:

**Always include:**
- The concept the learner's goal directly touches (if debugging auth, auth is in)
- Any concept that would surprise a newcomer (unusual patterns, non-obvious
  indirection, the thing that makes this codebase *this codebase* rather than
  a generic version of itself)
- The boundary between "stuff the learner's code calls" and "stuff that happens
  underneath" — this is usually where understanding breaks down

**Cut when tight on time:**
- Standard infrastructure the learner's stated stack already covers (if they
  know Express, don't teach what middleware is — mention it and move on)
- Logging, monitoring, error handling (unless the learner is debugging or
  unless the error handling IS the interesting part)
- Configuration/environment setup (a one-line mention is enough)
- Tests (unless the testing approach is architecturally significant)

**Never silently cut:**
- Anything the learner's stated goal needs
- Anything that would leave a gap in the trace (if step 3 depends on step 2's
  output, you can't cut step 2)

When you cut a concept, name it in the course's "what was left out" section
with a one-line reason. Selective is credible; silent omission is suspicious.

## 5 minimum, 9 maximum

Fewer than 5 means the trace was too shallow or the codebase is trivial enough
that a course isn't the right format — suggest reading the code directly instead.

More than 9 means either:
- The trace is too broad (you're covering multiple user actions, not one) — pick
  the one most relevant to the learner's goal and cut the rest.
- The concepts aren't distinct enough — two "functions that validate input" are
  one Gate concept with two examples, not two concepts.

## Ordering for the course

Don't default to execution order. Pick the order that teaches best:

- **Orient path:** Big picture first (what does this system even do?), then zoom
  into the trace. Start with Boundary or Pipeline shapes — they give the learner
  the map before the territory.
- **Debug path:** Start at the symptom, trace backward to the cause. The first
  module is "here's what's going wrong," not "here's how the system works."
- **Extend path:** Start at the nearest existing feature to what the learner
  wants to add, then show what it touches and where the new code would slot in.

See `branching-paths.md` for the full content-routing spec per path.

## When the codebase has no clear entry point

Some repos aren't apps — they're libraries, data pipelines, config-as-code,
or skill definitions (like this one). For these:

- **Libraries:** The entry point is the public API. Pick the most-used exported
  function and trace what happens when someone calls it.
- **Data pipelines:** The entry point is the trigger (a cron, a file drop, an
  API call). Trace one run of the pipeline.
- **Config/infra:** The entry point is "what happens when this config is
  applied" — a deploy, a build, a provision.
- **Skills/prompts:** The entry point is "someone invokes this." Trace the
  generation flow from trigger to output.

If genuinely nothing resembles an entry point, the codebase may be too
fragmented for a single-trace course — say so and offer to cover the 3-4 most
important files individually instead of forcing a false narrative of connection.
