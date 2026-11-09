# Diff mode

## Course state file

Every generated course writes a sidecar state file next to the HTML, same base name:
`my-project.course.json`. It records enough to detect and explain what changed next
time, without re-reading the whole repo from scratch.

```json
{
  "repo_snapshot": {
    "commit": "<git sha if available, else a content hash of tracked files>",
    "generated_at": "<ISO date>",
    "entry_points_traced": ["src/server.js:handleRequest", "..."],
    "concepts_covered": [
      {"id": "auth-middleware", "files": ["src/auth.js"], "module_slug": "how-requests-get-authenticated"},
      "..."
    ]
  },
  "learner": {
    "goal": "extend",
    "known_stack": ["javascript"],
    "time_budget": "20min"
  },
  "quiz_results": {
    "ledger-dedup": "missed",
    "gate-no-fabrication": "passed"
  }
}
```

If the repo has no git history, hash the traced files' contents instead of using a
commit SHA — still enough to detect "nothing changed" vs. "something changed."

`quiz_results` records pass/miss per concept id, taken from what the learner actually
clicked in the HTML (read it out of the page before regenerating, if the harness can
access the previous file — otherwise ask the learner which modules felt shaky). A
missed concept gets re-tested in the addendum even if its code didn't change at
all — the diff that matters isn't only in the repo, it's between what the learner
has demonstrated and what the course has covered. A concept marked "passed" is left
alone unless the diff shows its underlying code actually changed.

## On a new request against an existing state file

1. **Diff the snapshot.** Compare current file hashes/commit against the saved one
   for every file in `concepts_covered`, plus a quick re-scan for new files near the
   traced entry points.
2. **Classify the change:**
   - **Nothing changed** → tell the learner their course is still current, don't
     regenerate.
   - **Additive / localized** (a function's internals changed, a new field was added,
     a new route was added alongside existing ones) → **addendum mode.**
   - **Structural** (the entry point moved, a core abstraction was renamed or
     replaced, the traced flow no longer exists as described) → **full rebuild**,
     but say why: "the auth system was rewritten since your last course, so this is
     a full regenerate rather than a patch."
3. **Addendum mode output:** a short new module prepended to the existing course
   (don't regenerate modules that are still accurate), titled plainly, e.g. "What
   changed since your last course (Nov 9)." It should:
   - Name what changed, in the same code-to-English style as the rest of the course.
   - Explain *why* it matters given the learner's stated goal, not just what the diff
     says.
   - Link back to the original module(s) it supersedes or extends rather than
     repeating them.
   - Skip quizzes/animations unless the change is substantial enough to warrant one —
     addenda should be fast to consume, that's the whole point.
4. **Update the state file** after either path, so the next diff is against current
   state, not the original baseline.

## What counts as "the same course" vs. a new one

Diff mode only applies when it's reasonably the same learner coming back to the same
repo for roughly the same reason. If the stated goal has changed (was "just
understand it," now "I'm debugging a crash"), treat it as a new course for a new
purpose — reuse the concept map where it overlaps, but don't force a bug hunt into
an addendum to a tour.
