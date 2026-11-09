# codewalk

A Claude Code skill that turns a codebase into an interactive walkthrough: one HTML file, no dependencies, built around what you are trying to do with the code.

You built something with an AI agent and it works, but you can't say how. When it breaks, you end up asking the same agent to repair what it broke. Or you inherited a repo where the README says "run `npm start`" and that is all anyone knows.

Codewalk reads the repo, asks what you need from it, and builds a single page that explains how the code works. It has animations that run as you scroll, real code beside plain-English explanations, and quizzes that check whether you can apply what you read.

The output opens with a double-click, works offline, and needs no server.

## What makes it different

**It asks first.** Before building anything it asks four questions: what you are here to do, what you already know, how much time you have, and whether you want narration. Someone debugging gets different modules than someone getting oriented.

**It updates instead of rebuilding.** When the code changes, codewalk compares the repo with your last walkthrough. A small change gets a short addendum. A rewrite gets a full rebuild, with the reason. No change means it tells you and stops. Concepts you missed in the quizzes are tested again.

**Its metaphors come from a system.** Every concept in a codebase has a shape: gate, queue, cache, broadcast, lookup, pipeline, boundary, ledger, or scheduler. Codewalk classifies the shape first and then picks a metaphor from the codebase's own domain. A motorcycle news site gets pit-lane metaphors and a kitchen app gets prep-station ones. The same shape never gets the same metaphor twice, and each module carries a small icon for its shape.

**It has three paths.** Debug traces a failure from symptom to cause. Extend shows the pattern you are about to copy and where new code goes. Orient gives you the whole map. Modules shared between paths render once, and switching paths keeps your progress.

**It can narrate.** If you opt in, it writes a script and a sync map tied to scroll position, written to be heard and not just read. Any text-to-speech tool can play it.

## How it works

<p align="center">
  <img src="assets/flow.png" alt="The generation flow: intake, diff check, map the codebase, route into a branch, draw metaphors, build the HTML, save state" width="520">
</p>

The skill reads your codebase, traces one real user action from start to finish, and picks 5 to 9 concepts from that trace. It builds the page around the path you chose and writes a small JSON file next to the HTML so the next run can compare against it.

Everything it produces follows a few fixed rules:

- Code snippets are exact copies from the repo, linked to the file and line on GitHub.
- Quizzes test whether you can apply a mechanism, and a wrong answer leads to a simpler follow-up question.
- Animations start when you scroll to them, and every animation has a static version for reduced-motion settings.
- Light and dark mode are both supported.
- The last section lists what was left out and why.

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
Update my codewalk
```

The last one runs diff mode.

## What you get

Two files. `my-project.walkthrough.html` is the page. `my-project.walkthrough.json` is the saved state that diff mode reads.

## Skill layout

<p align="center">
  <img src="assets/tree.png" alt="Skill layout: SKILL.md and eight reference documents" width="520">
</p>

`SKILL.md` runs the generation flow. Each reference file is read only at the step that needs it, so the agent is never holding all of them at once.

## Credit

The core idea, turning a codebase into a single-file interactive HTML page with scroll-based modules, code-to-English translations, animated visualizations, and application-testing quizzes, comes from [codebase-to-course](https://github.com/zarazhangrui/codebase-to-course) by [Zara Zhang](https://x.com/zarazhangrui).

Codewalk is a reimplementation, not a fork. It adds personalized intake, diff mode, a structured metaphor bank, opt-in narration, and branching paths.

## License

MIT
