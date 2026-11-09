# Metaphor bank

The original rule — "never the same metaphor twice" — is right but unenforceable
without structure. This file gives it one: metaphors are organized by the *shape*
of the concept they explain, not by the concept itself, so the same shape can be
filled differently depending on the codebase's own domain.

## Why shape, not concept

"Auth is a bouncer checking IDs" is a fine metaphor exactly once, ever, across every
course this skill generates. The underlying shape — *a gate that checks a credential
before letting something through* — recurs constantly (auth, rate limits, feature
flags, validation middleware, permission checks). Organize by shape so a second
instance of that shape in the same course, or a future course, gets a *different*
surface metaphor for the same underlying move.

## Shape categories

For each concept the course needs to explain, first classify its shape, then pick
or mint a metaphor that fits both the shape and the codebase's own domain flavor.

- **Gate** — checks a credential/condition before letting something through
  (auth, validation, feature flags, permission checks, rate limiting)
- **Queue** — things wait their turn in order
  (job queues, event loops, message brokers, request buffering)
- **Cache** — a faster copy kept nearby to avoid redoing expensive work
  (memoization, CDN caching, database query caching)
- **Broadcast** — one thing announces, many things react without being asked
  (pub/sub, event emitters, webhooks, observer patterns)
- **Lookup** — a name or key resolves to a location or value
  (routing, DNS, dependency injection, database indexes)
- **Pipeline** — data moves through an ordered sequence of transformations
  (middleware chains, build steps, ETL, request/response processing)
- **Boundary** — a wall between two things that must not touch directly
  (API layers, sandboxing, client/server split, process isolation)
- **Ledger** — an append-only record of what happened, used to reconstruct state
  (event sourcing, git history, audit logs, transaction logs)
- **Scheduler** — decides what runs when, under constraints
  (cron, task queues, thread/process scheduling, CI pipelines)

If a concept doesn't fit any shape above, mint a new shape category rather than
forcing a bad fit — and add it to this list so future courses can reuse the category
(not the specific metaphor).

## Domain flavor

Once you have the shape, pick a surface metaphor that fits the *codebase's own
world*, not a generic one. A motorcycle media site's "Gate" concept should feel
different from a fintech app's "Gate" concept. Ask: what does this specific codebase
already evoke? Use that vocabulary.

Examples (illustrative, not a fixed list — mint your own per codebase):
- Motorcycle/racing domain: Gate → a pit-lane marshal checking a team's credentials
  before letting them onto the track. Queue → riders staged on the grid in qualifying
  order. Pipeline → a bike going through tech inspection, station by station.
- Kitchen/restaurant domain: Pipeline → an order ticket moving station to station.
  Queue → tickets on the rail, first in first out. Cache → mise en place, prepped
  ahead so the line doesn't stall.
- Library/archive domain: Lookup → the card catalog. Ledger → the circulation log.
  Boundary → the reading room that never lets originals leave the building.

## Within one course

Keep a running list, per course, of (shape, surface metaphor) pairs already used.
Before minting a metaphor for a new concept:
1. Classify its shape.
2. If that shape was already used in this course, the surface metaphor **must**
   differ — pick a different facet of the codebase's domain, don't reuse "pit lane"
   for every Gate in a racing-themed course.
3. If a concept is genuinely the *same* underlying mechanism reappearing (e.g. two
   different middleware functions that are both simple Gates), it's fine to say so
   explicitly ("this is the same kind of check you saw in module 2, just guarding a
   different door") rather than forcing a fresh metaphor on something that isn't
   conceptually new — that's more honest than manufacturing novelty.

## Retiring stale metaphors

A metaphor that's become a cliché across AI-generated explainers stops teaching and
starts reading as filler. Retire on sight rather than reach for these by default:
"bouncer checking IDs" for auth, "librarian/card catalog" for any lookup, "post
office" for any messaging system, "traffic cop" for any routing/gate. If the bank's
own domain-flavor examples above start feeling overused across many generated
courses, treat them the same way — replace with something sharper for that specific
codebase.
