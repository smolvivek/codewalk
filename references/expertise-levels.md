# Expertise levels

Codewalk is written first for people who build with AI agents and cannot read the code
that comes out. It also works for people who are learning to code and for engineers
who are new to a repo. Intake asks which description fits the reader, and the answer
changes most of the build.

## The four levels

| Id | Who | Default |
|---|---|---|
| `new` | Has not written code. Wants to understand what their project is made of. | |
| `vibe` | Builds with an AI agent. Knows what the app should do and cannot follow how it does it. | yes |
| `learner` | Writes some code and reads it with effort. Knows basic syntax in a language or two. | |
| `engineer` | Works in code professionally and is new to this repo or part of it. | |

If the reader does not say, use `vibe` and state the assumption in the line at the top
of the page. If their own messages show otherwise, for example they use words like
"middleware" or "idempotent" without explaining them, move up a level and say so.

## What each level changes

| | `new` | `vibe` | `learner` | `engineer` |
|---|---|---|---|---|
| Starts from | What the app does when a user acts | What the app does, then the code that causes it | The code, with the behavior question beside it | The design decision and its invariants |
| Code on screen | Short excerpts, shown after the explanation, each line glossed | Short excerpts, key lines highlighted | Full excerpts | Excerpts at the point of decision only |
| Vocabulary | Every term defined on first use | Terms defined on first use, then used normally | Only new terms defined | No definitions |
| Predictions ask about | Which plain-language outcome happens | What the app does, or what to tell the agent | Values and control flow | Design choices and failure modes |
| Metaphors | Every module | Most modules | Only shapes that are new to them | Only when the shape is not obvious |
| Apply questions | A scenario in app terms | "Your agent says X. What do you check?" | Change or extend a piece | Where this breaks and what you would change |
| Length | 5 to 6 modules | 6 to 8 | 6 to 9 | 5 to 7, dense |

## Rules at every level

- **Real code at every level.** The original-code rule holds for beginners too. A
  beginner gets fewer lines, never simplified lines.
- **Explain terms, not the reader.** No "simply," "just," or "obviously." Never
  suggest the reader should already know something.
- **Behavior before syntax at `new` and `vibe`.** Open each module with what happens
  in the running app, then show the code responsible.
- **Go deeper.** At `new`, `vibe`, and `learner`, each module has one collapsed "Go
  deeper" block written for the next level up. It is optional and never needed to
  follow the main text.
- **The level is stated on the page.** The first line says which level the page was
  built for. The reader can ask for a rebuild at another level.

## Known stack still applies

The level sets the baseline. The "what do you already know" answer from intake refines
it per concept. A `vibe` reader who says they know some React still gets full
treatment of the server side and a one-line mention of components.
