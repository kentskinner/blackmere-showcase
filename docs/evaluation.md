# Evaluation approach

Blackmere treats misleading prose as a system failure even when no state mutation occurs.

## Deterministic coverage

The private development repository currently contains 629 automated tests across the domain, perception, persistence, content, AI boundary, server, web application, and evaluation harness. Sixteen Playwright journeys exercise the application end to end.

Tests cover properties such as:

- rejected commands preserve the exact input state and emit no events;
- old or forged handles cannot be silently substituted;
- model responses generated against an old history head cannot commit;
- delayed narration or dialogue cannot repaint the UI after movement or undo;
- NPC conversation is gated independently at the server and domain boundaries by canonical presence and distance;
- undo rewinds consequences without granting a fresh random result;
- reconstruction reads committed history without replaying rules.

## Live-model evaluation

Live evaluation is intentionally opt-in and billable. Scenarios are versioned, the number of calls is planned before execution, and generated artifacts are reviewed independently rather than scored only by lexical rules.

The latest narrow Edda evaluation used three scenarios. Two were clean. The third contained a mild but real grounding failure: an unsupported implication that an investigation had found nothing. That result was recorded as **2/3 clean**, not rounded up.

This is not statistically sufficient to claim a general dialogue-grounding solution. It establishes that the production path can produce plausible bounded dialogue while also showing the exact class of error that still needs a stronger evidence mechanism.

## Containment is not correctness

Preventing model prose from mutating canonical state is necessary, but it is not enough. Players can still be misled by unsupported displayed text. The next grounding problem is therefore to validate assertions against structured evidence before display—not merely to keep invalid prose out of the database.
