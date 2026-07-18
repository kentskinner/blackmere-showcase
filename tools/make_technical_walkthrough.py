"""Rebuilds assets/blackmere-technical-walkthrough.gif from source/.

Composition-only: no live model call happens here. The Mara/Edda dialogue
lines are the exact recorded output from a real live playthrough (see
../source/dialogue-transcript.md); everything else (title cards, typed-out
player utterances, portrait framing) is presentation added when assembling
the GIF, not a claim about current production UI behavior.

Usage (from this directory):
    pip install -r requirements.txt
    python make_technical_walkthrough.py

Requires Windows-provided Segoe UI / Consolas fonts (see FONT paths below).
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent / "source"
OUT = ROOT.parent / "assets" / "blackmere-technical-walkthrough.gif"
W, H = 1280, 720

UI_INTRO = Image.open(SRC / "ui-intro.png").convert("RGB")
MAP_MARA = Image.open(SRC / "map-mara-visible.png").convert("RGB")
MAP_EDDA_AWAY = Image.open(SRC / "map-edda-away.png").convert("RGB")
MAP_EDDA_HERE = Image.open(SRC / "map-edda-colocated.png").convert("RGB")
MARA_PORTRAIT = Image.open(SRC / "mara-venn-portrait.jpg").convert("RGB")
EDDA_PORTRAIT = Image.open(SRC / "edda-vale-portrait.jpg").convert("RGB")

REG = r"C:\Windows\Fonts\segoeui.ttf"
BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
ITAL = r"C:\Windows\Fonts\segoeuii.ttf"
MONO = r"C:\Windows\Fonts\consola.ttf"
MONO_BOLD = r"C:\Windows\Fonts\consolab.ttf"


def f(size, bold=False, italic=False, mono=False):
    path = MONO_BOLD if mono and bold else MONO if mono else BOLD if bold else ITAL if italic else REG
    return ImageFont.truetype(path, size)


def cover(src, size=(W, H), x_bias=0.5, y_bias=0.5):
    scale = max(size[0] / src.width, size[1] / src.height)
    im = src.resize((round(src.width * scale), round(src.height * scale)), Image.Resampling.LANCZOS)
    left = round((im.width - size[0]) * x_bias)
    top = round((im.height - size[1]) * y_bias)
    return im.crop((left, top, left + size[0], top + size[1]))


def contain(src, box, bg=(14, 20, 29)):
    x, y, w, h = box
    scale = min(w / src.width, h / src.height)
    im = src.resize((round(src.width * scale), round(src.height * scale)), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (w, h), bg)
    canvas.paste(im, ((w - im.width) // 2, (h - im.height) // 2))
    return canvas


def lines(draw, text, font, max_w):
    result, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textbbox((0, 0), trial, font=font)[2] <= max_w:
            current = trial
        else:
            if current:
                result.append(current)
            current = word
    if current:
        result.append(current)
    return result


def text_block(draw, x, y, text, font, color, max_w, gap=7):
    lh = draw.textbbox((0, 0), "Ag", font=font)[3] + gap
    for line in lines(draw, text, font, max_w):
        draw.text((x, y), line, font=font, fill=color)
        y += lh
    return y


def shell(title, subtitle, step=None):
    im = Image.new("RGBA", (W, H), (11, 17, 25, 255))
    draw = ImageDraw.Draw(im)
    draw.rectangle((0, 0, W, 76), fill=(7, 11, 17, 255))
    draw.text((42, 22), "BLACKMERE", font=f(18, bold=True), fill=(234, 238, 233, 255))
    draw.text((170, 25), "// TECHNICAL WALKTHROUGH", font=f(12, mono=True), fill=(116, 151, 164, 255))
    if step:
        draw.text((1198, 24), step, font=f(13, bold=True, mono=True), fill=(207, 166, 100, 255))
    draw.text((42, 96), title, font=f(34, bold=True), fill=(241, 239, 224, 255))
    draw.text((44, 140), subtitle, font=f(16), fill=(155, 174, 178, 255))
    draw.rectangle((42, 686, 1238, 688), fill=(64, 84, 92, 255))
    return im


def card(draw, box, fill=(8, 14, 21, 235), outline=(70, 99, 110, 230)):
    draw.rounded_rectangle(box, radius=15, fill=fill, outline=outline, width=2)


def dim(bg, color, alpha):
    """Alpha-composites a solid overlay onto bg. Drawing a translucent
    rectangle directly with ImageDraw does not blend on an RGBA image — it
    replaces pixels outright — so this is required wherever a screenshot or
    portrait needs to stay partly visible under a darkening overlay."""
    overlay = Image.new("RGBA", bg.size, color + (alpha,))
    return Image.alpha_composite(bg.convert("RGBA"), overlay)


def badge(draw, x, y, label, value, accent=(107, 177, 204, 255), width=210):
    card(draw, (x, y, x + width, y + 62), (7, 13, 19, 235), (61, 88, 100, 220))
    draw.text((x + 16, y + 9), label.upper(), font=f(10, bold=True, mono=True), fill=(121, 145, 151, 255))
    draw.text((x + 16, y + 29), value, font=f(17, bold=True, mono=True), fill=accent)


def opening():
    bg = cover(UI_INTRO).filter(ImageFilter.GaussianBlur(1.2))
    bg = ImageEnhance.Brightness(bg).enhance(0.88).convert("RGBA")
    bg = dim(bg, (5, 9, 14), 90)
    draw = ImageDraw.Draw(bg)
    draw.text((58, 52), "BLACKMERE", font=f(22, bold=True), fill=(238, 240, 230, 255))
    draw.text((58, 95), "Grounded capture · current Stage 20 build", font=f(15, mono=True), fill=(126, 168, 183, 255))
    card(draw, (58, 490, 805, 640), (6, 11, 17, 226), (82, 112, 122, 220))
    draw.text((88, 522), "ONE MAP. TWO NPCS. COMMITTED WORLD STATE.", font=f(17, bold=True, mono=True), fill=(211, 170, 102, 255))
    draw.text((88, 560), "Every state change and dialogue line shown here is real.", font=f(23), fill=(234, 237, 229, 255))
    draw.text((88, 606), "Four live dialogue exchanges · claude-sonnet-5", font=f(14), fill=(137, 155, 158, 255))
    return bg


def movement():
    im = shell(
        "1. Movement changes what becomes possible",
        "The player starts at (2,8) and walks three ordinary grid steps to Mara.",
        "01/09",
    )
    draw = ImageDraw.Draw(im)
    map_panel = contain(MAP_MARA, (42, 184, 620, 470))
    im.paste(map_panel, (42, 184))
    draw.rounded_rectangle((42, 184, 662, 654), radius=16, outline=(69, 93, 102, 255), width=2)
    draw.text((60, 480), "Mara's canonical token — not a location marker", font=f(13, mono=True), fill=(211, 170, 102, 255))
    card(draw, (700, 184, 1238, 654))
    draw.text((732, 215), "COMMITTED EVENTS", font=f(13, bold=True, mono=True), fill=(118, 168, 187, 255))
    event_font = f(18, mono=True)
    events = [
        "move (2,8) -> (2,7)",
        "move (2,7) -> (2,6)",
        "move (2,6) -> (1,6)",
        "discover: Innkeeper Mara",
        "conversation available: true",
    ]
    y = 259
    for event in events:
        draw.text((734, y), event, font=event_font, fill=(220, 229, 226, 255))
        y += 43
    draw.text((734, 505), "No dialogue menu.", font=f(25, bold=True), fill=(240, 234, 214, 255))
    draw.text((734, 545), "Proximity unlocks free-text conversation.", font=f(19), fill=(165, 183, 184, 255))
    return im


def route_to_cottage():
    im = shell(
        "3. The map connects conversations",
        "Nine committed moves take Bran from Mara's inn to the cottage clearing.",
        "03/09",
    )
    draw = ImageDraw.Draw(im)
    map_panel = contain(MAP_EDDA_AWAY, (42, 184, 730, 470))
    im.paste(map_panel, (42, 184))
    draw.rounded_rectangle((42, 184, 772, 654), radius=16, outline=(69, 93, 102, 255), width=2)
    card(draw, (808, 184, 1238, 654))
    draw.text((838, 215), "AT THE CLEARING", font=f(13, bold=True, mono=True), fill=(119, 164, 182, 255))
    text_block(draw, 838, 263, "Edda does not appear to be home.", f(30, bold=True), (239, 236, 219, 255), 350, 8)
    badge(draw, 838, 405, "elapsed", "0 min", width=165)
    badge(draw, 1023, 405, "weather", "RAIN", (126, 177, 204, 255), 165)
    badge(draw, 838, 490, "Edda presence", "AWAY", (203, 138, 105, 255), 350)
    draw.text((838, 582), "No token rendered while away — wait is now available.", font=f(15, mono=True), fill=(167, 187, 185, 255))
    return im


def wait_diff(second=False):
    title = "5. The second wait changes NPC presence" if second else "4. Waiting is a domain command, not generated prose"
    subtitle = (
        "A second committed turn crosses Edda's authored arrival threshold."
        if second
        else "The first wait crosses only the weather threshold."
    )
    im = shell(title, subtitle, "05/09" if second else "04/09")
    draw = ImageDraw.Draw(im)
    src = MAP_EDDA_HERE if second else MAP_EDDA_AWAY
    map_panel = contain(src, (42, 184, 600, 470))
    im.paste(map_panel, (42, 184))
    draw.rounded_rectangle((42, 184, 642, 654), radius=16, outline=(69, 93, 102, 255), width=2)
    if second:
        draw.text((60, 480), "Player + Edda share a tile — 2 distinct tokens", font=f(13, mono=True), fill=(211, 170, 102, 255))
    card(draw, (680, 184, 1238, 654))
    draw.text((712, 214), "STATE DIFF", font=f(13, bold=True, mono=True), fill=(120, 169, 187, 255))
    rows = (
        [
            ("elapsedMinutes", "10 -> 20"),
            ("weather", "clearing"),
            ("Edda", "away -> at-position(5,12)"),
            ("conversation", "false -> true"),
            ("map render", "player + Edda, 2 tokens"),
        ]
        if second
        else [
            ("command", "wait-at-cottage-clearing"),
            ("elapsedMinutes", "0 -> 10"),
            ("weather", "rain -> clearing"),
            ("Edda", "away (unchanged)"),
        ]
    )
    y = 260
    for key, value in rows:
        draw.text((714, y), key, font=f(15, bold=True, mono=True), fill=(135, 153, 156, 255))
        draw.text((714, y + 25), value, font=f(20, mono=True), fill=(232, 235, 225, 255))
        y += 66 if second else 78
    draw.text((714, 586), "persistent · undoable · replayable", font=f(16, mono=True), fill=(208, 169, 103, 255))
    return im


def context_slide():
    im = shell(
        "7. The model sees bounded context",
        "The developer panel exposes exactly what Edda received for her second answer.",
        "07/09",
    )
    draw = ImageDraw.Draw(im)
    card(draw, (42, 184, 780, 654), (5, 10, 15, 245), (62, 91, 103, 230))
    code = [
        '"npc": {',
        '  "goal": "establish why an unfamiliar visitor',
        '           is waiting outside her cottage",',
        '  "voice": "Measured, direct, observant..."',
        "},",
        '"knownFacts": [',
        '  "A traveler ... went missing a week ago.",',
        '  "Blackmere has been unusually quiet ..."',
        "],",
        '"availableCommitments": [],',
        '"private knowledge redacted": 0',
    ]
    y = 214
    for line in code:
        color = (221, 230, 224, 255)
        if "knownFacts" in line:
            color = (113, 184, 211, 255)
        if "availableCommitments" in line:
            color = (212, 170, 104, 255)
        draw.text((70, y), line, font=f(17, mono=True), fill=color)
        y += 36
    card(draw, (814, 184, 1238, 654), (34, 29, 23, 240), (125, 105, 75, 230))
    draw.text((844, 215), "RECENT DIALOGUE", font=f(12, bold=True, mono=True), fill=(210, 171, 109, 255))
    text_block(draw, 844, 259, "Bran: I've been waiting for you.", f(19), (230, 236, 233, 255), 350)
    text_block(draw, 844, 341, "Edda: Waiting for me specifically, or just waiting?", f(19, italic=True), (240, 232, 211, 255), 350)
    draw.text((844, 475), "CURRENT UTTERANCE", font=f(12, bold=True, mono=True), fill=(126, 178, 198, 255))
    text_block(draw, 844, 516, "The village is very quiet. Is something wrong?", f(19), (230, 236, 233, 255), 350)
    return im


def limitation():
    im = shell(
        "8. Grounding is bounded, not solved",
        "The run is shown honestly—including a small unsupported assertion.",
        "08/09",
    )
    draw = ImageDraw.Draw(im)
    card(draw, (42, 184, 1238, 420), (40, 34, 27, 242), (131, 106, 72, 230))
    draw.text((72, 212), "EDDA'S ACTUAL RESPONSE", font=f(12, bold=True, mono=True), fill=(211, 172, 108, 255))
    draw.text((72, 263), "A traveler who stayed at the inn went missing a week back —", font=f(24, italic=True), fill=(241, 236, 218, 255))
    draw.rounded_rectangle((69, 304, 386, 351), radius=8, fill=(105, 46, 45, 235), outline=(186, 83, 76, 230), width=2)
    draw.text((82, 313), "no sign of them since", font=f(21, italic=True), fill=(255, 225, 219, 255))
    draw.text((399, 314), "← not entailed by either authored fact", font=f(17, mono=True), fill=(232, 155, 145, 255))
    card(draw, (42, 452, 594, 654), (7, 14, 20, 242), (65, 94, 106, 225))
    draw.text((72, 484), "ENGINE RESULT", font=f(12, bold=True, mono=True), fill=(119, 168, 187, 255))
    draw.text((72, 528), "accepted effects: []", font=f(20, mono=True), fill=(230, 235, 229, 255))
    draw.text((72, 570), "canonical state: unchanged", font=f(20, mono=True), fill=(230, 235, 229, 255))
    card(draw, (628, 452, 1238, 654), (28, 24, 20, 242), (117, 97, 70, 225))
    draw.text((658, 484), "KNOWN NEXT PROBLEM", font=f(12, bold=True, mono=True), fill=(211, 172, 108, 255))
    text_block(draw, 658, 526, "Detect unsupported assertions without turning dialogue into rigid templates.", f(23, bold=True), (241, 235, 217, 255), 520, 8)
    return im


def final():
    bg = cover(EDDA_PORTRAIT, (W, H), 0.58, 0.5)
    bg = ImageEnhance.Brightness(bg).enhance(0.5).convert("RGBA")
    bg = dim(bg, (3, 7, 11), 118)
    draw = ImageDraw.Draw(bg)
    draw.text((48, 42), "BLACKMERE", font=f(20, bold=True), fill=(236, 238, 228, 255))
    draw.text((48, 104), "WHAT EXISTS TODAY", font=f(14, bold=True, mono=True), fill=(118, 174, 194, 255))
    real = [
        "grid movement and discovery",
        "two distinct conversational NPCs",
        "canonical map tokens for visible NPCs (Stage 20)",
        "committed time, weather, and presence",
        "persistent, undoable turn history",
        "bounded effects and inspectable context",
    ]
    y = 148
    for item in real:
        draw.ellipse((52, y + 8, 62, y + 18), fill=(107, 177, 204, 255))
        draw.text((80, y), item, font=f(21), fill=(233, 237, 230, 255))
        y += 42
    card(draw, (48, 438, 775, 668), (7, 13, 18, 230), (75, 104, 113, 220))
    draw.text((78, 469), "NEXT PRESENTATION STEP", font=f(13, bold=True, mono=True), fill=(211, 172, 108, 255))
    next_y = text_block(
        draw,
        78,
        506,
        "NPC tokens currently snap to their canonical position each turn. Movement animation and pathfinding are deliberately deferred.",
        f(21, bold=True),
        (242, 237, 220, 255),
        650,
        6,
    )
    draw.text((78, next_y + 8), "The larger open problem remains dialogue grounding, above.", font=f(15, mono=True), fill=(154, 174, 174, 255))
    return bg


TYPE_STEPS = 8
TYPE_STEP_MS = 45
TYPE_HOLD_MS = 260
NPC_REPLY_HOLD_MS = 2600


def render_dialogue(title, subtitle, step, portrait, npc, revealed):
    """revealed: list of (speaker, display_text, full_text_for_sizing)."""
    im = shell(title, subtitle, step)
    draw = ImageDraw.Draw(im)
    art = cover(portrait, (410, 510), 0.72 if npc == "MARA VENN" else 0.75, 0.45)
    art = ImageEnhance.Brightness(art).enhance(0.76)
    im.paste(art, (42, 184))
    draw.rounded_rectangle((42, 184, 452, 694), radius=15, outline=(89, 102, 100, 255), width=2)
    draw.rectangle((42, 610, 452, 694), fill=(4, 8, 12, 215))
    draw.text((68, 629), npc, font=f(17, bold=True), fill=(236, 226, 200, 255))
    draw.text((68, 660), "actual live output", font=f(12, mono=True), fill=(127, 157, 165, 255))
    y = 184
    for speaker, display_text, full_text in revealed:
        is_player = speaker == "BRAN"
        box_h = 96 if len(full_text) < 78 else 125
        fill = (25, 58, 75, 235) if is_player else (48, 41, 31, 240)
        outline = (74, 129, 152, 230) if is_player else (134, 111, 76, 230)
        card(draw, (486, y, 1238, y + box_h), fill, outline)
        draw.text((510, y + 13), speaker, font=f(10, bold=True, mono=True), fill=(137, 190, 212, 255) if is_player else (213, 174, 111, 255))
        text_block(draw, 510, y + 38, display_text, f(19, italic=not is_player), (239, 244, 243, 255) if is_player else (242, 236, 218, 255), 700, 5)
        y += box_h + 14
    return im


def dialogue_animation(title, subtitle, step, portrait, npc, exchanges, first_note, later_note):
    """Builds a typewriter-animated sequence for one dialogue slide.

    exchanges: [(player_text, npc_text), (player_text, npc_text), ...]
    The player's line types out; the NPC's reply then appears whole
    (never typed, since it was never player-entered). This animation is
    composition-only — production Blackmere uses an ordinary text field,
    not typewriter playback.
    """
    frames = []
    revealed = []
    for i, (player_text, npc_text) in enumerate(exchanges):
        note = first_note if i == 0 else later_note
        for s in range(1, TYPE_STEPS + 1):
            n = max(1, round(len(player_text) * s / TYPE_STEPS))
            cursor = " |" if s < TYPE_STEPS else ""
            display = player_text[:n] + cursor
            frame_exchanges = revealed + [("BRAN", display, player_text)]
            im = render_dialogue(title, note, step, portrait, npc, frame_exchanges)
            frames.append((im, TYPE_STEP_MS if s < TYPE_STEPS else TYPE_HOLD_MS))
        revealed.append(("BRAN", player_text, player_text))
        revealed.append((npc, npc_text, npc_text))
        im = render_dialogue(title, note, step, portrait, npc, revealed)
        frames.append((im, NPC_REPLY_HOLD_MS))
    return frames


MARA_EXCHANGES = [
    ("What happened to the missing traveler?", "Don't know. Went out one night and didn't come back. That's all anyone can tell you."),
    (
        "You don't have to tell me. But you seem frightened.",
        "Frightened's a strong word. Careful, maybe. This place has had enough trouble without adding guesswork to it.",
    ),
]

EDDA_EXCHANGES = [
    ("I've been waiting for you.", "You've been waiting for me specifically, or just waiting?"),
    (
        "The village is very quiet. Is something wrong?",
        "A traveler went missing a week back. It's kept me watching the place closer than usual.",
    ),
]


def crossfade(a, b, steps=5, duration=80):
    out = []
    for step in range(1, steps + 1):
        out.append((Image.blend(a, b, step / steps), duration))
    return out


def quantize(im):
    return im.convert("P", palette=Image.Palette.ADAPTIVE, colors=120)


def build():
    timeline = []  # list of (RGBA image, duration_ms)

    def add(im, ms):
        timeline.append((im, ms))

    def add_seq(seq):
        timeline.extend(seq)

    def xfade_to(next_im, steps=5, duration=80):
        add_seq(crossfade(timeline[-1][0], next_im, steps, duration))

    op = opening()
    add(op, 4500)

    mv = movement()
    xfade_to(mv)
    add(mv, 5500)

    mara_slide_title = "2. Mara has her own voice and concealed knowledge"
    mara_frames = dialogue_animation(
        mara_slide_title,
        "NPC replies are exact; player prompts shortened only for layout.",
        "02/09",
        MARA_PORTRAIT,
        "MARA VENN",
        MARA_EXCHANGES,
        "Player utterance is typed for legibility — production uses an ordinary text field.",
        "NPC replies are exact; player prompts shortened only for layout.",
    )
    xfade_to(mara_frames[0][0])
    add_seq(mara_frames)

    rc = route_to_cottage()
    xfade_to(rc)
    add(rc, 5800)

    w1 = wait_diff(False)
    xfade_to(w1)
    add(w1, 5800)

    w2 = wait_diff(True)
    xfade_to(w2)
    add(w2, 7000)

    edda_slide_title = "6. Edda is a second character, not a reskinned Mara"
    edda_frames = dialogue_animation(
        edda_slide_title,
        "Player utterance is typed for legibility — production uses an ordinary text field.",
        "06/09",
        EDDA_PORTRAIT,
        "EDDA VALE",
        EDDA_EXCHANGES,
        "Player utterance is typed for legibility — production uses an ordinary text field.",
        "Live response excerpts; the source transcript preserves the exact text.",
    )
    xfade_to(edda_frames[0][0])
    add_seq(edda_frames)

    cx = context_slide()
    xfade_to(cx)
    add(cx, 8500)

    lm = limitation()
    xfade_to(lm)
    add(lm, 8500)

    fn = final()
    xfade_to(fn)
    add(fn, 8000)

    frames = [quantize(im) for im, _ in timeline]
    durations = [ms for _, ms in timeline]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        OUT,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=1,
    )
    total_s = sum(durations) / 1000
    print(f"{OUT} — {len(frames)} frames, {total_s:.1f}s total")


if __name__ == "__main__":
    build()
