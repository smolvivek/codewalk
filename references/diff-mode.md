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

`quiz_results` records pass/miss per concept id. Since the HTML is a static file
with no server, the course writes quiz state to `localStorage` as the learner
answers (key: `codewalk-quiz-{repo-name}`), and also embeds a "Copy my progress"
button in the course footer that copies the full quiz_results JSON object to the
clipboard — one click, plain text, pasteable.

When the agent runs diff mode:
1. **Best case — the agent can read the HTML file.** The course embeds a
   `<script type="application/json" id="quiz-state">` block that the page's JS
   updates on each answer. If the agent has access to the saved HTML file (i.e.
   the learner saved after completing quizzes, or the browser cached the updated
   DOM), read quiz_results directly from that block.
2. **Fallback — ask the learner.** If the embedded state is empty or the agent
   can't access the file, ask: "Which modules felt solid and which felt shaky?"
   Two to three words per module is enough to reconstruct pass/miss. Don't make
   the learner re-take a quiz — they already did the work.
3. **Clipboard paste.** If the learner used "Copy my progress," they can paste
   it directly when asked. The agent parses the JSON and populates quiz_results.

A missed concept gets re-tested in the addendum even if its code didn't change at
all — the diff that matters isn't only in the repo, it's between what the learner
has demonstrated and what the course has covered. A concept marked "passed" is left
alone unless the diff shows its underlying code actually changed.

### Implementation in the HTML

The page JS must:
- On each quiz answer, write `{conceptId: "passed"|"missed"}` to both
  `localStorage` and the embedded `#quiz-state` JSON block.
- Wrap all `localStorage` access in try/catch (private browsing, storage full).
- On page load, restore quiz state from `localStorage` if available (so
  returning to the page shows which quizzes were already completed).
- The "Copy my progress" button in the footer serializes the current
  quiz_results object as formatted JSON and calls `navigator.clipboard.writeText`.

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
