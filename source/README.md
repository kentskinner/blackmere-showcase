# Source material for the technical walkthrough

Every file here is an input to `tools/make_technical_walkthrough.py`. Three
provenance categories, kept distinct throughout the walkthrough and its
documentation:

1. **Recorded live dialogue transcript.** The Mara and Edda lines used in
   the walkthrough are verbatim excerpts from one real live-model playthrough
   (dialogue model `claude-sonnet-5`), recorded in `dialogue-transcript.md` in this
   directory. Complete responses remain in that transcript; the composition
   shortens some lines only by omission. That capture is not reproduced by
   this generator, and no new live/billable call happens when the GIF is
   rebuilt.
2. **Application screenshots from the Stage 19/20 development build**, all
   captured under the deterministic stub provider (no live model call):
   - `ui-intro.png` — a pre-Stage-20 intro-modal capture; this UI was
     unchanged by the token stage.
   - `map-mara-visible.png` — Mara's canonical amber "M" token, visible on
     the map once in sight (Stage 20).
   - `map-edda-away.png` — a pre-Stage-20 capture of the cottage clearing
     while Edda is canonically `away`; it remains accurate because an away
     NPC does not render a token.
   - `map-edda-colocated.png` — the player and Edda's canonical positions
     co-located at the same tile, rendered as two small, legible, distinct
     tokens (Stage 20A's co-location fix).
3. **Generated portrait/background art**, used only as decorative
   composition for the dialogue slides — never presented as current
   in-game UI:
   - `mara-venn-portrait.jpg`
   - `edda-vale-portrait.jpg`

`dialogue-transcript.md` also records the honest grounding note: Edda's
reply contains one unsupported implication ("no sign of them since") that
the engine accepted no effect for. The walkthrough preserves this beat
deliberately.
