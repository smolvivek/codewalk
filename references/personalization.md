# Personalization

Two readers should not get the same walkthrough of the same repo. Ask before
building, and skip a question only if the original request already answered it.

## Intake questions

Ask these in one short message, not as a form.

1. **Which of these fits you best?** Read out the four levels from
   `expertise-levels.md` in plain language. Default to `vibe` if no answer comes.
2. **What are you here to do?** Debug something specific, add or change a feature,
   or just understand how it works. Take free text too.
3. **What do you already know?** One open question works better than a skill-level
   dropdown: "Which of these languages or frameworks are you comfortable with? Is
   there anything I should not re-explain?" Use the answer to refine per-concept
   depth within the chosen level.
4. **Narration?** Yes or no, default no. See `narration.md`.
5. **How much time do you have?** A rough budget (10 minutes, 30 minutes, no limit).
   It sets module count and depth more than it sets which concepts appear.

If the user only says "turn this into a walkthrough," default to `vibe` level,
the Orient path, no assumed knowledge of the stack, no narration, and a 20-minute
budget. Do not wait on an unanswered question. Generate with those defaults and
state what you assumed in one line at the top of the page, with a way to
regenerate.

## How answers change the build

- **Level sets the baseline.** See `expertise-levels.md` for what each level
  changes: how much code appears, what the predictions ask about, whether terms
  are defined, and what the apply questions test. The level is stated on the
  first line of the page.
- **Goal sets the branch.** Debugging or a specific task goes to Debug. Adding or
  changing goes to Extend. Open-ended goes to Orient. See `branching-paths.md`.
- **Known stack refines depth within the level.** For each concept in the trace,
  decide whether the reader already knows it (one-line mention, then move on) or
  does not (full module with the learning loop). Do not ask about each concept.
  Infer from the stated background and from what is idiomatic: someone
  comfortable in React does not need `useState` explained, but someone who only
  mentioned Python might. A `vibe` reader who says they know some React still
  gets full treatment of the server side.
- **Time budget sets module count.** When time is short, go broader and shallower
  on background concepts and keep full depth on whatever the goal requires. Never
  drop something the goal needs to fit the budget. Say so instead: "There is a
  queueing system here too. I skipped it because it is outside what you are
  changing. Ask if you want it covered."

## State the assumptions

Every walkthrough opens with one plain line giving the level, assumed goal,
background, and time budget, and how to change them. It is text, not a settings
panel:

> Built for: vibe coder adding a feature. Assumes you know what the app should
> do but not how the code works. About 20 minutes.
> If that is wrong, tell me and I will rebuild it.
