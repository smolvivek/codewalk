# Narration

Optional, opt-in at intake. When on, each module gets a short narration script and
a sync map, instead of (or alongside) the on-page text.

## Script style

Write for the ear, not the eye. The on-page text and the narration script are not
the same text read two ways — write narration as its own draft:

- Contractions, shorter sentences, no parenthetical asides (a listener can't re-read
  a clause). Say "this part's a bit different" not "this part (unlike the previous
  one) differs."
- Narration can point at what's on screen rather than re-describing it: "watch the
  left side light up" works in audio; it doesn't work in silent text.
- One idea per sentence. A script that sounds like a teleprompter reading dense prose
  aloud has failed — go back and simplify rather than shorten by deleting words.
- Keep the same no-recycled-metaphor and shape-first system from `metaphor-bank.md`;
  narration explains the same concepts, it doesn't get its own looser set of
  metaphors.
- Each module's script should run roughly 30-90 seconds spoken — long enough to
  cover the module, short enough that losing your place and scrolling back costs
  nothing.

## Sync format

Narration doesn't need to be pre-recorded — the course ships a script and a sync
map, and the learner can have it read aloud by whatever TTS they have, or read it
themselves. The sync map ties narration segments to scroll position so playback
(if the learner wires up audio) can auto-advance the page, or so a simple "read
along" highlight can track a learner reading it manually.

Emit as a JSON block embedded in the page (not a separate file, so the course stays
single-file):

```html
<script type="application/json" id="narration-sync">
{
  "modules": [
    {
      "slug": "how-requests-get-authenticated",
      "segments": [
        {"text": "Every request that hits this server passes through one check first.", "anchor": "#auth-step-1"},
        {"text": "That check lives in auth dot js, and it's doing one simple thing.", "anchor": "#auth-step-2"}
      ]
    }
  ]
}
</script>
```

`anchor` points at an element id already present in the module for the visualization
or code block that segment is narrating, so a read-along highlight or auto-scroll
can use the existing DOM rather than new markup.

## What this is not

Not a requirement to actually synthesize audio — that's outside what a static HTML
file can self-contain anyway. The deliverable is the script plus the sync map; the
learner (or a separate step, if the harness has TTS available) turns it into audio
if they want it. The page should degrade gracefully with the script simply available
as readable text (e.g. in a collapsible "narration" toggle per module) when no audio
is wired up.
