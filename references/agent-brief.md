# Plan and agent brief

The last module of a walkthrough has two parts. The reader writes their own plan, then
sees a reference plan and a ready-to-paste brief for their coding agent. The order
matters. Handing over a finished prompt first would teach the reader to delegate, which
is the habit this skill exists to break.

## Part 1: your plan

Ask: "What do you want to change or fix? Write your plan in 3 to 5 steps, and name the
files you expect to touch. Do this before scrolling down."

- A text area saved to localStorage (key `codewalk-plan-{repo-name}`).
- A "Show the reference plan" button. It works with an empty plan and records the plan
  as skipped. Nothing is locked.
- If the reader's goal was Orient, ask for a change they might want to make someday, or
  "what would you want to ask your agent to build next?"

## Part 2: the reference plan

Show 3 to 5 steps built from the concept map. Each step:

- names a real file and function
- links to the module that explains it
- says what the step changes and what it should leave alone

State the assumption about the goal in one line, since the reference plan is only as
good as the goal it was written for.

Next to each step the reader marks **had it**, **partly**, or **missed it**. The marks
are saved with the progress object. Missed steps get a link back to their module.

## Part 3: the brief

A block of text with a Copy button, shown after Part 2. The page assembles it from the
concept map and from the reader's own progress. Template:

```
Goal: {the reader's goal, one sentence}

How this codebase works (checked against the code):
- {concept}: {one sentence}. See {file path}.
{one line per concept in the path}

Where the change goes:
- {file and function}: {why}

Leave alone:
- {what the change should not touch, and why}

How to check it worked:
- {a command to run or behavior to observe, with the expected result}

Before you edit anything, explain these back to me in plain language, because I was
unsure about them:
- {concepts the reader missed or marked "guessing" or "think so" and got wrong}

Then make the change in small steps and tell me what each step did.
```

Rules for the brief:

- Every fact comes from the concept map or the recorded trace. If a claim is only read
  from the code, the brief says "from reading the code."
- The "explain these back to me" section is filled in by the page's script from the
  progress object. If the reader missed nothing, omit that section and its lead-in.
- The last line stays. It asks the agent to explain as it works, so the reader keeps
  following along.
- Put the real paths on the brief element as `data-paths="src/a.js,src/b.js"`, so the
  verify script can check they exist.
- Level changes the wording. At `new` and `vibe`, use plain language and add "Ask me to
  confirm before running anything that deletes or overwrites files." At `engineer`, keep
  it compact and drop the plain-language framing.

## Checking the plan in the session

If the reader pastes their plan into the chat, compare it with the reference plan.
Reply with the steps they had, the steps they missed, and one question about the
biggest gap. Do not rewrite their plan for them.
