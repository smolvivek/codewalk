# Codebase mapping

How to read a codebase you have never seen and decide what to teach. This step sits
between intake (who is reading, what they want) and writing (modules, metaphors,
visuals). If it goes wrong, the walkthrough teaches the wrong things with confidence.

## Find the entry point

Every codebase has at least one place where a user does something and the code
responds. That is the entry point. It is the place where a real action enters the
system, which is not always `main()` or `index.js`.

Look in this order, from most to least reliable:

1. **README or docs.** Most repos say "run this, then visit localhost:3000" or "this
   script does X." That is the action.
2. **Scripts and commands.** `package.json` scripts, Makefile targets, CLI entry
   points, and CI workflows show what the developer actually runs.
3. **Route handlers and API definitions.** For a web app, grep for route definitions
   (Express `app.get`, FastAPI `@app.route`, Rails `routes.rb`) and pick the most
   common or most representative one.
4. **Main function.** The fallback: `if __name__ == "__main__"`, `func main()`, or the
   top-level code that runs on import.

If the reader is debugging something specific, their bug report is the entry point.
Trace from where the symptom appears, not from where the code starts.

If the reader wants to extend something, the entry point is the existing feature
nearest to what they want to add.

## Trace one action end to end

Start at the entry point and follow exactly one user action through the code. Do not
cover everything the app can do.

Read in execution order, not file order:

1. Start at the entry point function or handler.
2. For each call it makes, open that function and read it.
3. Note each distinct thing that happens: a check, a transformation, a storage
   operation, a message sent, a response returned.
4. Stop when the action completes, meaning a response is sent, a file is written, or
   the process exits.

Keep a running list with a shape beside each step:

```
entry: POST /api/digest -> handleDigest()
  -> loadConfig()           [Lookup: resolves user preferences]
  -> fetchSources()         [Boundary: calls external APIs]
  -> deduplicateItems()     [Ledger: checks what has been seen before]
  -> formatDigest()         [Pipeline: turns raw items into readable output]
  -> deliver()              [Pipeline: sends through the configured channel]
```

That list, with shapes attached, is the concept map.

## Choose 5 to 9 concepts

A trace usually finds more concepts than a walkthrough should cover. Filter them.

**Always include:**

- The concept the reader's goal touches directly. If they are debugging auth, auth is
  in.
- Anything that would surprise a newcomer: unusual patterns, indirection that is not
  obvious, whatever makes this codebase different from a generic one.
- The boundary between what the reader's own code calls and what happens underneath.
  Understanding usually breaks down there.

**Cut when time is short:**

- Standard infrastructure the reader's stack already covers. If they know Express,
  mention middleware and move on.
- Logging, monitoring, and error handling, unless the reader is debugging or the error
  handling is the interesting part.
- Configuration and environment setup. One line is enough.
- Tests, unless the testing approach is central to the architecture.

**Never cut silently:**

- Anything the reader's goal needs.
- Anything that would leave a gap in the trace. If step 3 depends on step 2's output,
  step 2 stays.

When you cut a concept, name it in the "What was left out" section with a one-line
reason. Naming what was cut is credible. Omitting it silently looks like a mistake.

## Five minimum, nine maximum

Fewer than five means the trace was too shallow, or the codebase is small enough that
a walkthrough is the wrong format. Suggest reading the code directly.

More than nine means one of two things:

- The trace is too broad and covers several user actions. Pick the one most relevant
  to the reader's goal and cut the rest.
- The concepts are not distinct. Two functions that validate input are one Gate with
  two examples, not two concepts.

## Order

Do not default to execution order. Pick the order that teaches best.

- **Orient.** Big picture first: what does this system do? Then zoom into the trace.
  Start with a Boundary or Pipeline, which give the reader the map before the
  territory.
- **Debug.** Start at the symptom and trace back to the cause. The first module says
  what is going wrong. It does not explain how the system works.
- **Extend.** Start at the existing feature nearest to the new one, then show what it
  touches and where the new code would go.

See `branching-paths.md` for the full spec per path.

## When there is no clear entry point

Some repos are not apps. They are libraries, data pipelines, infrastructure config, or
skill definitions.

- **Libraries.** The entry point is the public API. Pick the most used exported
  function and trace a call.
- **Data pipelines.** The entry point is the trigger: a cron job, a file drop, an API
  call. Trace one run.
- **Config and infrastructure.** The entry point is what happens when the config is
  applied: a deploy, a build, a provision.
- **Skills and prompts.** The entry point is someone invoking it. Trace the flow from
  trigger to output.

If nothing resembles an entry point, the codebase may be too fragmented for a single
trace. Say so, and offer to cover the three or four most important files one by one
instead of inventing a story that connects them.
