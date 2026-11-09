# Personalization

Two readers should not get the same walkthrough of the same repo. Ask before
building, and skip a question only if the original request already answered it.

## Intake questions

Ask these in one short message, not as a form.

1. **What are you here to do?** Debug something specific, add or change a feature,
   or just understand how it works. Take free text too.
2. **What do you already know?** One open question works better than a skill-level
   dropdown: "Which of these languages or frameworks are you comfortable with? Is
   there anything I should not re-explain?" Use the answer to decide, per concept,
   whether it gets a full module, a one-line mention, or a link to the docs.
3. **Narration?** Yes or no, default no. See `narration.md`.
4. **How much time do you have?** A rough budget (10 minutes, 30 minutes, no limit).
   It sets module count and depth more than it sets which concepts appear.

If the user only says "turn this into a walkthrough," default to the Orient path,
no assumed knowledge of the stack, no narration, and a 20-minute budget. Do not
wait on an unanswered question. Generate with those defaults and state what you
assumed in one line at the top of the page, with a way to regenerate.

## How answers change the build

- **Goal sets the branch.** Debugging or a specific task goes to Debug. Adding or
  changing goes to Extend. Open-ended goes to Orient. See `branching-paths.md`.
- **Known stack sets concept depth.** For each concept in the trace, decide whether
  the reader already knows it (one-line mention, then move on) or does not (full
  module with metaphor, code and English, visualization, and quiz). Do not ask about
  each concept. Infer from the stated background and from what is idiomatic: someone
  comfortable in React does not need `useState` explained, but someone who only
  mentioned Python might.
- **Time budget sets module count.** When time is short, go broader and shallower on
  background concepts and keep full depth on whatever the goal requires. Never drop
  something the goal needs to fit the budget. Say so instead: "There is a queueing
  system here too. I skipped it because it is outside what you are changing. Ask if
  you want it covered."

## State the assumptions

Every walkthrough opens with one plain line giving the assumed goal, background, and
time budget, and how to change them. It is text, not a settings panel:

> Built for: adding a feature. Assumes you know JS but not Python. About 20 minutes.
> If that's wrong, tell me and I'll rebuild it.
