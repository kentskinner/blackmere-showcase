# Recorded live dialogue transcript

Captured from one clean playthrough of the Stage 19/20 development build on
2026-07-18. Dialogue model: `claude-sonnet-5`. Four live dialogue exchanges
were generated for this capture; nothing here is invented or replayed by the
generator. The walkthrough embeds verbatim excerpts of these lines, shortening
only by omission for layout, and rebuilding the GIF makes no new model call.

## Live actions taken during capture

- Began a new game.
- Walked from `(2,8)` to Mara at `(1,5)` and made two live dialogue
  exchanges.
- Walked through the map to the clearing adjacent to Edda's Cottage.
- Waited twice through the real `wait-at-cottage-clearing` domain command.
- Observed weather clearing at 10 elapsed minutes.
- Observed Edda's presence change from `away` to `at-position (5,12)` at 20
  elapsed minutes.
- Made two live dialogue exchanges with Edda.

## Exact Mara output

> **Bran:** Good afternoon. I'm Bran. What happened to the missing
> traveler?
>
> **Mara:** Don't know. Went out one night and didn't come back. That's all
> anyone can tell you.

> **Bran:** You don't have to tell me. But you seem frightened.
>
> **Mara:** Frightened's a strong word. Careful, maybe. This place has had
> enough trouble without adding guesswork to it.

Expression: `flat gaze, arms crossed`.

## Exact Edda output

> **Bran:** Good afternoon. I'm Bran. I've been waiting for you.
>
> **Edda:** Afternoon. Edda Vale — I keep watch on this village. You've been
> waiting for me specifically, or just waiting?

Expression: `steady, appraising look`.

> **Bran:** The village is very quiet. Is something wrong?
>
> **Edda:** You noticed that too. A traveler who stayed at the inn went
> missing a week back — no sign of them since. It's kept me watching the
> place closer than usual. Now, you said you were waiting for me. What's
> this about?

Expression: `steady gaze, unhurried`.

## Honest grounding note

Edda's model-visible context contained two authored facts:

1. A traveler who stayed at the inn went missing a week ago.
2. Blackmere has been unusually quiet since the traveler went missing, and
   Edda has been keeping a closer watch.

The phrase "no sign of them since" is not entailed by either fact. The
engine accepted no effect from that line, and canonical state stayed
unchanged. The walkthrough preserves this beat deliberately — it is the
same known grounding-failure class recorded during the engine's own live
evaluation, not a defect hidden from viewers.
