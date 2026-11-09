# Personalization

The same repo should not produce the same course for two different learners. Ask
before building. Skip a question only if the learner's original request already
answered it.

## Intake questions (ask as one short batch, not a form)

1. **What are you here to do?**
   - Debug something specific right now
   - Add or change a feature
   - Just understand how this works, no immediate task
   - (free text — take whatever they give you)

2. **What do you already know?**
   One open question beats a skill-level dropdown: *"Any of these languages/frameworks
   already comfortable for you? Anything you'd rather I not re-explain?"* Use the
   answer to decide, per concept, whether it gets full treatment, a one-line mention,
   or is skipped with a link to docs instead.

3. **Narration?** (see `narration.md`) — yes/no, defaults to no.

4. **How much time do you have?** — rough budget (10 min / 30 min / no limit) that
   controls module count and depth more than it controls which concepts are covered.

If the learner just says "turn this into a course" with nothing else, default to:
Orient path, assume no prior knowledge of the stack, no narration, ~20-minute budget.
Don't block on an unanswered question — generate with sane defaults and say what you
assumed in one line at the top of the course, with an easy way to regenerate if the
assumption was wrong.

## How answers reshape generation

- **Goal → branch.** Debug/specific task → Debug path. Add/change → Extend path.
  Open-ended → Orient path. (See SKILL.md "Branching paths.")
- **Known stack → concept depth.** For each concept the trace touches, classify it
  as "learner already knows this" (one-line mention + skip) vs. "new to them" (full
  module: metaphor, code-to-English, visualization, quiz). Don't ask about every
  concept individually — infer from their stated background plus what's idiomatic
  to assume (someone comfortable in React doesn't need `useState` explained even if
  they didn't say so explicitly; someone who only mentioned Python might).
- **Time budget → module count, not coverage gaps.** If the budget is tight, go
  broader-shallower on background concepts and keep full depth only on whatever the
  stated goal directly requires. Never silently drop something the goal needs to fit
  a time budget — say so instead ("there's a queueing system here too, skipping it
  since it's outside what you're changing — ask if you want it covered").

## One line of transparency

Every generated course opens with a single line stating what was assumed (goal,
background, time budget) and how to change it — not a settings panel, just plain
text: *"Built for: adding a feature, assuming you know JS but not Python, ~20 min.
Wrong? Tell me and I'll rebuild."*
