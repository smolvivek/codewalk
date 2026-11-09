# Diff mode

## State file

Every walkthrough writes a state file next to the HTML with the same base name:
`my-project.walkthrough.json`. It records enough to detect and explain what changed
next time without re-reading the whole repo.

```json
{
  "repo_snapshot": {
    "commit": "<git sha if available, else a content hash of tracked files>",
    "generated_at": "<ISO date>",
    "entry_points_traced": ["src/server.js:handleRequest"],
    "concepts_covered": [
      {"id": "auth-middleware", "files": ["src/auth.js"], "module_slug": "how-requests-get-authenticated"}
    ]
  },
  "reader": {
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

If the repo has no git history, hash the contents of the traced files instead of
using a commit SHA. That is still enough to tell "nothing changed" from "something
changed."

## Quiz state

`quiz_results` records passed or missed per concept id. The HTML is a static file with
no server, so the page stores quiz state itself and offers three ways for the agent to
get it back. Try them in this order:

1. **Embedded state.** The page keeps a
   `<script type="application/json" id="quiz-state">` block up to date on each answer.
   If the agent can read the saved HTML file (the reader saved the page after taking
   the quizzes, or the browser cached the updated page), read `quiz_results` from that
   block.
2. **Pasted state.** The footer has a "Copy my progress" button that copies the full
   `quiz_results` object as JSON. If the reader used it, ask them to paste it, parse
   it, and fill in `quiz_results`.
3. **Ask the reader.** If neither works, ask which modules felt solid and which felt
   shaky. Two or three words per module is enough to reconstruct passed and missed.
   Do not make them retake a quiz.

A missed concept gets re-tested in the addendum even if its code did not change. The
useful diff is partly in the repo and partly between what the reader has shown they
understand and what the walkthrough covered. A passed concept is left alone unless its
underlying code changed.

### What the page must do

- On each quiz answer, write `{conceptId: "passed" | "missed"}` to both `localStorage`
  (key: `codewalk-quiz-{repo-name}`) and the embedded `#quiz-state` block.
- Wrap all `localStorage` access in try/catch, for private browsing and full storage.
- On load, restore quiz state from `localStorage` when it is available, so a returning
  reader sees which quizzes they finished.
- Make the footer "Copy my progress" button serialize the current `quiz_results` as
  formatted JSON and call `navigator.clipboard.writeText`.

## When a state file already exists

1. **Diff the snapshot.** Compare the current file hashes or commit against the saved
   ones for every file in `concepts_covered`. Also scan for new files near the traced
   entry points.
2. **Classify the change.**
   - **Nothing changed.** Tell the reader their walkthrough is still current. Do not
     regenerate.
   - **Additive or local.** A function's internals changed, a field was added, or a
     route was added next to existing ones. Use **addendum mode**.
   - **Structural.** The entry point moved, a core abstraction was renamed or
     replaced, or the traced flow no longer exists as described. Do a **full
     rebuild**, and say why: "The auth system was rewritten since your last
     walkthrough, so this is a full rebuild and not a patch."
3. **Addendum output.** Add one short module at the top of the existing walkthrough.
   Leave modules that are still accurate alone. Give it a plain title, for example
   "What changed since your last walkthrough (Nov 9)." It should:
   - Name what changed, in the same code and English style as the rest.
   - Explain why it matters for the reader's goal, beyond what the diff says.
   - Link to the original modules it extends or replaces instead of repeating them.
   - Skip quizzes and animations unless the change is large enough to need one. An
     addendum should be quick to read.
4. **Update the state file** after either path, so the next diff compares against
   current state and not the original.

## Same walkthrough or a new one

Diff mode applies when it is roughly the same reader returning to the same repo for
roughly the same reason. If the goal changed, for example from "just understand it" to
"I'm debugging a crash," treat it as a new walkthrough. Reuse the concept map where
it overlaps, but do not force a bug hunt into an addendum on a tour.
