# codewalk

A Claude Code skill that turns a codebase into an interactive walkthrough. One HTML file, no dependencies, built around what you actually need to know.

You built something with an AI agent and it works, but you cannot explain how. When it breaks, you end up asking the same agent to repair what it broke, and you have no way to tell if the fix is good. Or you inherited a repo and the README says "run `npm start`" and that is all anyone wrote down.

Codewalk reads the repo, asks what you need from it, and builds a single page that teaches how the code works. It asks you to predict what happens before showing you, records what you get wrong, and ends with a brief you can paste into your agent so it knows what you learned.

The output opens with a double-click, works offline, and needs no server.

## Who it is for

Codewalk has four expertise levels. The default is vibe coder.

| Level | Who |
|---|---|
| **New** | Has not written code. Wants to understand what their project is made of. |
| **Vibe** (default) | Builds with an AI agent. Knows what the app should do but cannot follow how it does it. |
| **Learner** | Writes some code and reads it with effort. Knows basic syntax in a language or two. |
| **Engineer** | Works in code professionally and is new to this repo or part of it. |

The level changes what code appears on screen, how terms are defined, what the predictions ask about, and how apply questions are framed. A vibe coder's prediction asks "what does the app do here?" An engineer's asks "what design choice was made and what breaks if you change it?"

At every level, code on screen is the real code from the repo, never simplified.

## How it teaches

The design follows a simple idea: the reader should think before the page explains. Anthropic ran a randomized trial with 52 engineers and found that those who delegated the work to an AI scored around 50% on comprehension, while those who worked through problems themselves scored around 67% ([study](https://www.anthropic.com/research/AI-assistance-coding-skills)). The study was small and tested a chat assistant, not this format. Treat it as a reason for the design, not as proof of it.

Every module follows the same loop:

1. **Frame.** One sentence naming the question.
2. **Predict.** The reader picks an answer and marks their confidence (guessing, think so, or sure) before anything is revealed.
3. **Reveal.** What actually happens. If the code was run, this shows the recorded trace. If not, it says so.
4. **Explain.** The metaphor, the code, and the plain English.
5. **Apply.** A question in a new situation. A wrong answer gets a simpler follow-up.

A confident wrong answer is the most useful signal the page can record. Concepts the reader was sure about and got wrong appear in a "Where your picture was off" section and are retested first if the walkthrough is rebuilt.

## Observed vs Read

Codewalk tries to run the code in a scratch copy of the repo before building the page. When it can, each module's values and replays come from the recorded run, and the module carries an **Observed** badge with the commit and date. When it cannot (missing dependencies, no safe way to run it), the module is labeled **Read**: explained from the code, not verified by running it. Every module says which one it is.

## Three paths

**Orient** gives you the whole map. **Debug** traces a failure from symptom to cause. **Extend** shows the pattern you are about to copy and where new code goes. Modules shared between paths render once, and switching paths keeps your progress.

## Plan and agent brief

The last module asks you to write your own plan before showing a reference plan built from the concept map. You mark each reference step as "had it," "partly," or "missed it." Then a copyable agent brief appears, assembled from the concepts and your progress, including a line that asks the agent to explain back anything you got wrong. The plan comes before the brief on purpose: handing over a finished prompt first would teach the reader to delegate, which is the habit this skill exists to break.

## Change mode

Say "explain this PR" or "what did my agent change" and codewalk builds a page about the diff instead of the codebase. It groups changes by behavior (not by file), runs the same action on the base and the head when possible, walks you through each change with predictions, and ends with a verdict section and a copyable block of questions to ask your agent.

## Diff mode

When the code changes, codewalk compares the repo with your last walkthrough. A small change gets a short addendum. A rewrite gets a full rebuild, with the reason stated. No change means it tells you and stops. Concepts you missed are retested first.

## How it works

<p align="center">
  <img src="assets/flow.png" alt="The generation flow: intake, diff check, map, route, classify, observe, build, plan and brief, verify" width="520">
</p>

The skill reads your codebase, traces one real user action from start to finish, and picks 5 to 9 concepts from that trace. It runs the action in a scratch copy to get real values. It builds the page around the path you chose and writes a small JSON file next to the HTML so the next run can compare against it. A verify script checks the output before handing it back.

Fixed rules across every walkthrough:

- Code snippets are exact copies from the repo, linked to the file and line on GitHub.
- Predictions come before explanations. The metaphor never appears before the prediction.
- Every module carries an Observed or Read badge.
- Animations start when you scroll to them, and every animation has a static version for reduced-motion settings.
- Light and dark mode are both supported.
- The last sections are "Where your picture was off" and "What was left out."

## Install

```bash
cp -r codewalk/ ~/.claude/skills/
```

Then open a project in Claude Code and say one of these:

```
Walk me through this codebase
Turn this into a walkthrough
Teach me how this code works
I'm debugging the login flow, make me a codewalk
What did my agent change
Explain this PR
Update my codewalk
```

## What you get

Two files. `my-project.walkthrough.html` is the page. `my-project.walkthrough.json` is the saved state that diff mode reads.

In change mode: one file, `my-project.changes.html`.

## Skill layout

<p align="center">
  <img src="assets/tree.png" alt="Skill layout: SKILL.md, thirteen reference documents, and a verify script" width="520">
</p>

`SKILL.md` runs the generation flow. Each reference file is read only at the step that needs it, so the agent is never holding all of them at once.

## Credit

The core idea, turning a codebase into a single-file interactive HTML page with scroll-based modules, code-to-English translations, and animated visualizations, comes from [codebase-to-course](https://github.com/zarazhangrui/codebase-to-course) by [Zara Zhang](https://x.com/zarazhangrui).

Codewalk is a reimplementation, not a fork. It adds four expertise levels, a predict-before-reveal learning loop, observed-versus-read provenance, a plan-then-brief closing module, change mode, diff mode, a structured metaphor bank, opt-in narration, and branching paths.

## License

MIT
