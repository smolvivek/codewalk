# Learning loop

Every module follows the same loop. The reader commits to a guess before anything is
explained, then sees what the code actually does, then applies it somewhere new. This
file explains why and sets the rules.

## Why

Anthropic ran a randomized trial with 52 mostly junior engineers learning an unfamiliar
Python library
([AI assistance and coding skills](https://www.anthropic.com/research/AI-assistance-coding-skills)).
Those who used an AI assistant scored about 50% on a comprehension quiz, against about
67% for those who coded by hand, and the biggest gap was on debugging questions. How
people used the assistant mattered more than whether they used it. Those who delegated
the work or leaned on the AI to fix errors scored under 40%. Those who asked why and
how, or worked through errors themselves, scored 65% or higher.

The study was small and used a chat assistant, and nobody has tested this format. Treat
it as a reason for the design, not as proof of it. The design consequence is that the
reader should do the thinking before the page supplies the answer, and a page that only
explains makes that easy to skip.

## The loop

1. **Frame.** One sentence naming the question this module answers. No explanation yet.
2. **Predict.** The reader commits to an answer before anything is revealed.
3. **Reveal.** Show what actually happens: the real code, the replay or the read, and
   the real value next to the reader's guess.
4. **Explain.** Now the metaphor and the code and English. Short.
5. **Apply.** A question in a new situation that needs the mechanism just shown.

Every module has Frame, Predict, Reveal, and Explain. Apply appears on every module the
reader's goal touches directly, and on at least half of all modules.

The metaphor never comes before the prediction. A metaphor in the frame primes the
answer and makes the prediction meaningless.

## Predict

- Choose one of two to four options. The page cannot grade free text, so do not ask
  for it.
- Wrong options come from real misunderstandings of the mechanism, not from jokes.
- Include "I don't know" as a valid option. It counts as skipped and is never
  penalized. Nothing is gated behind a correct answer.
- The question must be answerable from what the reader has already seen plus ordinary
  reasoning. Do not ask about something the page has not set up.
- Ask about something the reveal will show: a real value from the trace, a behavior, or
  a location in the code. The level sets the kind (see `expertise-levels.md`).
- The choice locks when the reader commits.

## Confidence

The reader marks one of three levels with each choice: **guessing**, **think so**,
**sure**. Committing needs both a choice and a confidence mark.

A wrong answer held with high confidence is the most useful thing the page can learn
about a reader. Record it and use it (see Scoring).

## Reveal

- Show whether the guess matched, in one plain line. A wrong guess is not scolded.
  Say what actually happens.
- Show the real value beside the guess. If the module is Observed, the replay shows the
  recorded run. If it is Read, say so (see `ground-truth.md`).

## Apply

- Use a new situation, not the same example as the reveal.
- A wrong answer triggers one simpler, more concrete follow-up that isolates the
  misunderstanding, before the page moves on.
- Feedback is one line saying why, tied to the code or diagram on screen.

## Break it

Used on the Debug path and anywhere a failure teaches the mechanism better than a
success.

1. Show a failure, either a real symptom the reader gave or a deliberate break.
2. The reader picks where it originates from a list of real locations, with a
   confidence mark.
3. The trace shows the real origin.

A deliberate break ("what happens if this check is deleted?") is only labeled Observed
if it was actually run in a scratch copy. Otherwise it is labeled Read.

## Scoring

Per concept, store three values:

```json
{"prediction": "right", "apply": "missed", "confidence": "sure"}
```

- `prediction`: `right`, `wrong`, or `skipped`
- `apply`: `passed`, `missed`, or `n/a`
- `confidence`: `guessing`, `think-so`, or `sure`

A **confident miss** is `confidence: "sure"` with a wrong prediction or a missed apply.

Use the results in two places:

- The last section of the page lists "Where your picture was off," confident misses
  first, each linking to its module.
- Diff mode retests confident misses first, then other misses, then unsure passes. A
  confident pass is left alone (see `diff-mode.md`).

## Not allowed

- No timers, streaks, points, or numeric scores.
- No blocking progress until an answer is right.
- No trick questions and no questions about trivia.
- No question that can be answered by pattern matching on the page's wording.
