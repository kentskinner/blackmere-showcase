# Source material for the technical walkthrough

Every file here is an input to `tools/make_technical_walkthrough.py`. Three
provenance categories, kept distinct throughout the walkthrough and its
documentation:

1. **Recorded live dialogue transcript.** The exact Mara and Edda lines used
   in the walkthrough came from one real live-model playthrough (dialogue
   model `claude-sonnet-5`), recorded in `dialogue-transcript.md` in this
   directory. That capture is not reproduced by this generator — the lines
   are embedded as text in `tools/make_technical_walkthrough.py`. No new
   live/billable call happens when the GIF is rebuilt.
2. **Current application screenshots**, captured against the running
   Stage 20 build under the deterministic stub provider (no live model
   call):
   - `ui-intro.png` — the intro modal.
   - `map-mara-visible.png` — Mara's canonical amber "M" token, visible on
     the map once in sight (Stage 20).
   - `map-edda-away.png` — the cottage clearing while Edda is canonically
     `away` (no token renders — this is correct fog/presence behavior, not
     a missing feature).
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
