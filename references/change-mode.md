# Change mode

Explains a change instead of a codebase: a pull request, a commit range, a branch, or
"what my agent just changed." The question the reader has is "what did it do, and is it
safe to keep?" The page answers it with the same loop as a walkthrough.

Use this file when the request is about a diff. Steps 1, 5, 6, 7, and 10 of the main
flow still apply. Steps 3 and 4 are replaced by the process below.

## Trigger phrases

"Explain this PR," "what did my agent change," "what changed since yesterday," "review
this diff," "is this safe to merge."

## Get the diff

In order of preference:

1. A PR number or URL: `gh pr diff`. If that is unavailable, fetch the branch and use
   local git.
2. A commit range or branch against its base: `git diff base...head`.
3. Uncommitted work: `git diff HEAD`, plus untracked files from `git status`.

Always read the full diff before writing anything. If it is too large to read (more
than a few thousand changed lines), say so and ask which part matters most.

## Intake

Ask two things, as one short message:

1. Which level fits you? (see `expertise-levels.md`; default `vibe`)
2. What do you need to decide: whether to merge it, how it works, or what broke?

## Group by behavior, not by file

Read the diff and sort changes into groups. Each group is one change in behavior,
whatever files it touches. Collect formatting, lockfiles, renames, and generated files
into a single "Housekeeping" line and do not teach them.

For each group record:

- **What it does**, in one plain sentence.
- **Its shape** (see `metaphor-bank.md`), and the kind of risk that shape carries:

| Shape | What to look for |
|---|---|
| Gate | A check loosened, removed, moved, or bypassed |
| Ledger | State written, read, or deleted differently |
| Boundary | A new crossing between layers or services |
| Cache | New or removed invalidation |
| Queue, Scheduler | Changed ordering, retry, or timing |
| Lookup | A key, route, or name that now resolves differently |
| Pipeline, Broadcast | A step added, removed, or reordered |

- **How to verify it**: a concrete check the reader can run or observe, with the
  expected result.

Aim for 3 to 8 groups. If there are more, merge groups that share a mechanism.

## Observe both sides

If the action can be run, run the same action and input on the base and on the head,
each in its own scratch worktree (see `ground-truth.md`), and record both traces. The
page shows them side by side and highlights where they diverge. A divergence the reader
did not expect is the most valuable thing the page can show.

If it cannot be run, label every module Read.

## Build with the loop

Each group becomes one module.

1. **Frame.** "This change touches the login check."
2. **Predict.** "Does this make login stricter, looser, or the same?" or "What do you
   expect to differ in the output?" With a confidence mark.
3. **Reveal.** The diff with the changed lines marked, and the trace difference if it
   was observed.
4. **Explain.** What changed and why it might matter. Metaphor if the level calls for it.

There is no branch switcher. The module order is: the change the reader said matters
most first, then the riskiest, then the rest.

## Closing module

1. **Your verdict.** The reader picks **merge**, **merge after fixes**, or **do not
   merge**, with a confidence mark, before anything is shown.
2. **Findings.** Each finding cites diff lines and carries one of three labels:
   **Must check**, **Worth checking**, or **Fine**. Each says whether it was Observed
   or Read.
3. **Questions to ask your agent.** A copyable block in the style of `agent-brief.md`,
   including "Explain why you changed {X}" for each group the reader got wrong.

## Honesty line

The page opens with one sentence: "This explains the change. It does not guarantee the
change is safe." Findings only claim what the diff or the trace shows. Do not guess at
behavior outside the changed code.

## Output

Write `{repo}.changes.html`. There is no state file. The same verify script runs with
`--mode changes`.
