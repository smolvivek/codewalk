# Narration

Optional, and chosen at intake. When it is on, each module gets a short script
and a sync map, in addition to the on-page text.

## Script style

Write for the ear. The on-page text and the script are two separate drafts, not
one text read two ways.

- Use contractions and short sentences. Avoid parenthetical asides, because a
  listener cannot re-read a clause. Say "this part's a bit different," not "this
  part (unlike the previous one) differs."
- Point at what is on screen instead of re-describing it. "Watch the left side
  light up" works in audio and fails in silent text.
- One idea per sentence. If the script sounds like a teleprompter reading dense
  prose, simplify the ideas. Do not just delete words.
- Use the same shapes and the same no-repeat rule from `metaphor-bank.md`.
  Narration explains the same concepts with the same metaphors.
- Aim for 30 to 90 seconds spoken per module. That covers the module, and losing
  your place costs little.

## Predict-step cues

Before each prediction card, the narration script includes a pause cue:

> "Before I show you what happens next, take a guess. Look at the options on
> screen and pick the one that fits."

The segment's `anchor` points at the prediction card's element. This gives the
reader time to think before the reveal, which is the point of predict-before-
reveal. Without the cue, a listener who is following along may hear the answer
before they see the question.

After the reveal:

> "Here is what actually happens."

Keep the cue short. One sentence before, one sentence after. The card handles
the rest.

## Sync format

Nothing is pre-recorded. The walkthrough ships a script and a sync map. The
reader can run the script through any text-to-speech tool or read it themselves.
The sync map ties each segment to a scroll position, so playback can advance
the page, or a read-along highlight can follow a reader.

Embed the map as a JSON block in the page, not a separate file, so the
walkthrough stays one file:

```html
<script type="application/json" id="narration-sync">
{
  "modules": [
    {
      "slug": "how-requests-get-authenticated",
      "segments": [
        {"text": "Every request that hits this server passes through one check first.", "anchor": "#auth-step-1"},
        {"text": "Before I show you what happens next, take a guess.", "anchor": "#auth-predict"},
        {"text": "Here is what actually happens.", "anchor": "#auth-reveal"},
        {"text": "That check lives in auth dot js, and it is doing one simple thing.", "anchor": "#auth-step-2"}
      ]
    }
  ]
}
</script>
```

`anchor` is the id of an element already in the module, such as the
visualization, prediction card, or code block that segment describes. A highlight
or auto-scroll can then use the existing DOM without new markup.

## Limits

This does not produce audio. A static HTML file cannot contain synthesized
speech. The deliverable is the script and the sync map. Without audio, the page
still works: the script is available as text in a collapsible narration toggle
on each module.
