# Architecture

Blackmere is built around a strict authority boundary:

> The engine owns facts, rules, memory, time, presence, and consequences. The model interprets language and performs the fiction.

## Governing pipeline

```text
player intent
→ bounded interpretation
→ engine-supplied legal action
→ validation
→ deterministic rules or recorded random result
→ atomic canonical commit
→ grounded narration
```

The order matters. Narration happens after a turn has committed. A narration failure cannot roll back the canonical result, and regenerating prose cannot rerun rules.

## Canonical state

The implemented vertical slice records, among other things:

- player position and explored space;
- perceived and discovered information;
- elapsed time and current ambient condition;
- whether an NPC is away or at an exact map position;
- per-NPC memories, beliefs, and important reported facts;
- resolved investigations and their recorded random outcomes;
- committed events and one-step undo history.

State changes pass through domain commands. Unknown handles, unavailable actions, stale model responses, and effects outside an NPC's authored capabilities are rejected rather than silently repaired or substituted.

## Model context

The language model does not receive a raw dump of the world. Each feature constructs a purpose-specific semantic projection containing only relevant, authorized information.

For NPC dialogue this includes the addressed NPC's authored identity, goals, voice guidance, known facts, memories, current scene, and bounded legal effects. Mara's concealed knowledge and Edda's public knowledge therefore follow different paths even though they share the same conversation infrastructure.

## A concrete sequence

1. Edda begins canonically `away`.
2. At her cottage, the player may choose one authored **Wait a while** action.
3. The first wait advances the clock by ten minutes and changes rain to clearing.
4. The second wait advances another ten minutes and moves Edda to her exact cottage position.
5. The conversation surface becomes available because canonical presence and distance now allow it.
6. Moving away or undoing invalidates any delayed dialogue response, preventing stale prose from repainting or committing against a newer world state.

This is intentionally a bounded example, not a claim of general continuous simulation.

## Why this architecture

Language models are excellent at interpretation and performance, but plausible prose is not reliable storage. Separating those roles gives the system somewhere definitive to answer questions such as:

- Did this event actually happen?
- Does this NPC know it happened?
- Is the NPC reporting knowledge, belief, rumor, or deception?
- Was this random outcome already revealed before undo?
- Is the speaker physically present?
- Did the model merely say something, or did the engine accept a consequence?

The resulting world is more constrained than a free-form chatbot, but substantially more inspectable and resilient.
