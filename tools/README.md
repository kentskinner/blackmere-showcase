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

`make_technical_walkthrough.py` deterministically writes
`../assets/blackmere-technical-walkthrough.gif`. `verify_walkthrough.py`
re-reads that file and checks:

- dimensions are exactly 1280×720;
- the GIF loops (`loop == 0`);
- frame count is at least 20;
- total duration is between 60 and 90 seconds;

and prints the exact frame count, duration, and file size it measured. It
exits non-zero if any check fails.

## What's in `source/`

See `../source/README.md` for the three provenance categories (recorded
live dialogue transcript, current deterministic-build screenshots, and
generated portrait/background art) and exactly which file is which.

## Changing the walkthrough

- Dialogue text lives in `MARA_EXCHANGES` / `EDDA_EXCHANGES` at the top of
  `make_technical_walkthrough.py` — keep it byte-for-byte matched to
  `../source/dialogue-transcript.md` if you touch it, since that transcript
  is the record of what was actually said.
- Map/UI screenshots are the `MAP_*` / `UI_INTRO` constants — swap the
  `../source/*.png` files and re-run the build to refresh them from a newer
  engine build.
- The typewriter animation (`dialogue_animation`) is composition only. It
  is not a claim that production Blackmere has typewriter playback — it
  currently uses an ordinary text field.
