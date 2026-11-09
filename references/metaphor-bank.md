# Metaphor bank

"Never use the same metaphor twice" is a good rule that nobody can follow without
structure. This file adds the structure. Metaphors are filed by the shape of the
concept they explain, so the same shape can be filled differently depending on the
codebase's own domain.

## Why shape

"Auth is a bouncer checking IDs" works once. The shape underneath it, a gate that
checks a credential before letting something through, shows up constantly: auth,
rate limits, feature flags, validation middleware, permission checks. Filing by
shape means a second gate in the same walkthrough, or in a later one, gets a
different surface metaphor for the same move.

## Shapes

For each concept, classify its shape first. Then pick or invent a metaphor that fits
both the shape and the codebase's domain.

- **Gate.** Checks a credential or condition before letting something through.
  Auth, validation, feature flags, permission checks, rate limiting.
- **Queue.** Things wait their turn in order. Job queues, event loops, message
  brokers, request buffering.
- **Cache.** A faster copy kept nearby to avoid repeating expensive work.
  Memoization, CDN caching, query caching.
- **Broadcast.** One thing announces and many things react without being asked.
  Pub/sub, event emitters, webhooks, observers.
- **Lookup.** A name or key resolves to a location or value. Routing, DNS,
  dependency injection, database indexes.
- **Pipeline.** Data moves through an ordered series of transformations.
  Middleware chains, build steps, ETL, request and response processing.
- **Boundary.** A wall between two things that must not touch directly. API layers,
  sandboxing, the client and server split, process isolation.
- **Ledger.** An append-only record of what happened, used to rebuild state. Event
  sourcing, git history, audit logs, transaction logs.
- **Scheduler.** Decides what runs when, under constraints. Cron, task queues,
  thread scheduling, CI pipelines.

If a concept fits none of these, add a new shape to this list rather than forcing a
bad fit. Future walkthroughs can reuse the shape, though not the metaphor.

## Domain flavor

Once you have the shape, pick a surface metaphor from the codebase's own world. A
gate in a motorcycle media site should feel different from a gate in a fintech app.
Ask what this codebase already evokes, and borrow that vocabulary.

These examples are illustrations. Invent your own for each codebase.

- Motorcycle racing: a gate is a pit-lane marshal checking a team's credentials
  before they enter the track. A queue is riders staged on the grid in qualifying
  order. A pipeline is a bike moving through tech inspection one station at a time.
- Restaurant kitchen: a pipeline is an order ticket moving from station to station.
  A queue is tickets on the rail, first in first out. A cache is mise en place,
  prepped ahead so the line does not stall.
- Archive: a lookup is the finding aid. A ledger is the accession log. A boundary is
  the reading room that never lets originals leave the building.

## Within one walkthrough

Keep a running list of the (shape, surface metaphor) pairs already used. Before
writing a metaphor for a new concept:

1. Classify its shape.
2. If that shape was already used, the surface metaphor must differ. Use another
   part of the domain. Do not reuse the pit lane for every gate in a racing
   walkthrough.
3. If the concept is the same mechanism showing up again, such as two middleware
   functions that are both simple gates, say so: "This is the same kind of check as
   in module 2, guarding a different door." That is more accurate than inventing
   novelty.

## Retired metaphors

Some metaphors are now so common in generated explanations that they read as filler.
Do not reach for them: a bouncer checking IDs for auth, a librarian or card catalog
for any lookup, a post office for any messaging system, a traffic cop for any
routing or gate. If the domain examples above start to feel overused, treat them
the same way and find something sharper for the codebase at hand.
