# Walkthrough

The showcase GIF was assembled from a single clean playthrough of the current development build.

## Sequence

1. Start a new game as Bran.
2. Walk from the inn entrance to Mara.
3. Ask Mara about the missing traveler and whether she is frightened.
4. Walk through the inn and outside to Edda Vale's cottage.
5. Observe that Edda is canonically away and no conversation control is offered.
6. Wait ten minutes. The committed ambient condition changes from rain to clearing.
7. Wait another ten minutes. Edda's canonical presence changes from `away` to her cottage position.
8. Speak with Edda about having waited and about the unusual quiet in Blackmere.
9. Inspect the model-visible context and compare Edda's reply with the authored facts.

## Why the final inspection matters

Edda's reply contains one unsupported implication: “no sign of them since.” Her supplied facts establish that a traveler went missing about a week ago and that she has kept a closer watch; they do not establish that anyone searched or found no evidence.

The walkthrough retains this failure. It illustrates both the remaining research problem and an existing safety property: the line does not become canonical merely because the model said it, and Edda had no legal state-changing effect available in that exchange.

## What is real and what is presentation

The movements, waits, state transitions, conversations, and displayed debug context came from the running application. The generated character portraits and explanatory title cards were added when composing the GIF. They are visual framing, not a claim that the current game UI already contains illustrated portraits or cinematic presentation.
