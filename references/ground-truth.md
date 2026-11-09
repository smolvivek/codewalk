# Ground truth

An explanation written from reading code can be confident and wrong. This step reduces
that by running the traced action once and recording what really happens. Animations
replay the recording, and quiz values come from it. Anything that was not run is
labeled as read.

Run this step after mapping and before building. Everything here applies to change mode
as well.

## Two labels

Every module carries one provenance label on its `data-provenance` attribute and as a
badge next to its title.

- **Observed.** The module's replay and values come from a recorded run in this
  session. Tooltip: "Replayed from a real run on {date} at {commit}."
- **Read.** The module is explained from the code and was not executed. Tooltip:
  "Explained from the code. Not run."

If a module mixes both, label the module by its weakest part and mark the observed
values individually in the text. Never label a module Observed because a neighboring
module was.

## How to run

Work from least to most invasive.

1. An existing test, script, or dry-run flag that exercises the action.
2. A small driver script, written in the scratch directory, that calls the entry point
   with a fixture input.
3. The real command, traced by a profiler or by logging added in a scratch copy.

Always work in a scratch copy of the repo (`git worktree add` or a plain copy into a
temp directory). Never instrument the reader's working tree. Delete the copy when done.
Run with a timeout of 60 seconds unless the action needs longer, and with a minimal
environment: no production credentials.

A minimal Python tracer for option 3:

```python
import os, sys

ROOT = os.getcwd()
events = []

def trace(frame, event, arg):
    if event in ("call", "return") and frame.f_code.co_filename.startswith(ROOT):
        value = frame.f_locals if event == "call" else arg
        events.append({
            "event": event,
            "function": frame.f_code.co_name,
            "file": os.path.relpath(frame.f_code.co_filename, ROOT),
            "line": frame.f_lineno,
            "value": repr(value)[:200],
        })

sys.setprofile(trace)
# call the entry point here
sys.setprofile(None)
```

For other languages, add one log line at entry and exit of each function in the concept
map, in the scratch copy, or use the language's own tracing facility.

## Ask before running

Stop and ask the reader first if the action would:

- call a network service that is not on localhost
- touch a database that is not a local or test database
- send an email, message, or payment, or post anywhere
- delete or write files outside the scratch directory
- need credentials the reader has not offered for this purpose

Prefer a dry-run flag, a mock, or a fixture over asking. If none of those is possible
and the reader does not approve, do not run it. Mark the affected modules Read.

## What to record

For each step in the trace that maps to a concept, record the call, the file and line,
and the input and output. Keep 3 to 12 steps per module.

Make the recording safe before it goes anywhere near the page:

- Replace the value of any key matching `key`, `token`, `secret`, `password`, `auth`,
  `cookie`, or `session` with `"[redacted]"`.
- Replace anything that looks like a credential: AWS key IDs, `sk-` keys, GitHub
  tokens, private key blocks, bearer tokens.
- Replace real personal data, such as emails, names, and phone numbers, with obvious
  placeholders.
- Truncate strings over 200 characters and lists over 5 items, and set `"truncated":
  true` on the step.

## Embedding

Embed the recording in the page as one JSON block:

```html
<script type="application/json" id="trace-data">
{
  "run": {
    "command": "python scripts/process.py --dry-run",
    "commit": "7ff0522",
    "at": "2026-11-09T09:40:00Z",
    "environment": "scratch copy, no network"
  },
  "steps": [
    {
      "id": "s1",
      "concept": "dedup-ledger",
      "call": "deduplicate_items",
      "file": "scripts/process.py",
      "line": 41,
      "input": {"items": 12},
      "output": {"kept": 9, "dropped": 3},
      "truncated": false
    }
  ]
}
</script>
```

Each Observed module lists its step ids in `data-trace-steps="s1,s2"`. The animations
read their frames from these steps. Do not hard-code values in the animation that are
not in the trace.

## Using the recording

- **Replays.** Data-flow and conversation animations step through the recorded
  calls. The dot that moves through a pipeline carries the recorded payload.
- **Predictions.** The reader predicts a recorded value, then the reveal shows it.
- **Apply questions.** Use recorded values as the inputs of the new situation where
  possible.
- **Deliberate breaks.** To ask "what happens if this is removed?", make the change in
  the scratch copy, run it again, and record the result. If the break was not run, the
  question is Read.

## When the code cannot be run

Missing dependencies, no way to run it without real services, or a library with no
entry point to call. Do not guess at a trace. Mark every module Read, say so in the
line at the top of the page ("Nothing here was run. Explanations come from reading the
code."), and continue.

## Check afterward

`scripts/verify_walkthrough.py` checks that every trace step points at a real file and
line, that every Observed module lists real step ids, and that the trace holds no
credential patterns. Run it before handing back.
