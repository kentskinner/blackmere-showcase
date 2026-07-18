# Technical walkthrough generator

Rebuilds `assets/blackmere-technical-walkthrough.gif` from the source
material in `../source/`. Composition-only — running this makes no model
call and costs nothing. Windows-oriented (uses Windows-provided Segoe UI /
Consolas fonts).

## Build

```
cd tools
pip install -r requirements.txt
python make_technical_walkthrough.py
python verify_walkthrough.py
```

`make_technical_walkthrough.py` writes
`../assets/blackmere-technical-walkthrough.gif`. GIF palette encoding bytes
can vary between runs even when the decoded animation is identical, so
`verify_walkthrough.py` checks the decoded visual/timing result rather than
the container's byte hash:

- dimensions are exactly 1280×720;
- the GIF loops (`loop == 0`);
- frame count is at least 20;
- total duration is between 60 and 90 seconds;
- the RGBA pixels and frame durations match the reviewed walkthrough digest;

and prints the exact frame count, duration, and file size it measured. It
exits non-zero if any check fails.

After an intentional visual change, inspect the rebuilt frames before updating
`EXPECTED_DECODED_SHA256` in the verifier to the newly reviewed digest.

## What's in `source/`

See `../source/README.md` for the three provenance categories (recorded
live dialogue transcript, Stage 19/20 deterministic-build screenshots, and
generated portrait/background art) and exactly which file is which.

## Changing the walkthrough

- Dialogue text lives in `MARA_EXCHANGES` / `EDDA_EXCHANGES` at the top of
  `make_technical_walkthrough.py`. Every displayed line must be a verbatim,
  contiguous excerpt of `../source/dialogue-transcript.md`; do not paraphrase
  or recombine it. The transcript is the record of each complete response.
- Map/UI screenshots are the `MAP_*` / `UI_INTRO` constants — swap the
  `../source/*.png` files and re-run the build to refresh them from a newer
  engine build.
- The typewriter animation (`dialogue_animation`) is composition only. It
  is not a claim that production Blackmere has typewriter playback — it
  currently uses an ordinary text field.
