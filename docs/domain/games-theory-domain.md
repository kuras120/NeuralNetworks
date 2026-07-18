# Game Theory Domain

This document defines the durable language, boundaries, and invariants of the turn-based Q-learning domain.

## Bounded Contexts

| Context | Responsibility |
| --- | --- |
| Game Interface | Accepts the current board and score, then returns the selected move as a public coordinate. |
| State Normalization | Converts external board symbols into a bot-relative canonical representation. |
| Learning | Evaluates the previous transition, maintains Q-values, and selects the next legal action. |
| Persistence | Stores configuration, a pending previous move, and learned transition quality across invocations. |

## Ubiquitous Language

- **Board state**: flattened board passed by the caller in row-major order using external symbols (`X`, `O`, `N`).
- **Canonical state**: internal bot-relative state where `-1 = bot`, `1 = opponent`, and `0 = empty`.
- **Neighbour state**: legal next canonical state generated from the current state by placing the bot marker.
- **Move coordinate**: zero-based `{x, y}` location of the bot marker added by the selected neighbour state; `(0, 0)` is the top-left cell, `x` increases rightward, and `y` increases downward.
- **Q-table**: persisted transition-quality map keyed by canonical state, then by candidate next state.
- **Last move**: pending transition saved after a bot move and consumed on the next invocation after the opponent move.
- **Reward**: delta of bot advantage between the previous pending move and the current observed state.

## Domain Rules

- `X` always starts in the external game, but the bot may be either `X` or `O`; runtime logic must use `ai-char` to normalize state.
- Q-learning data must stay independent from the external bot symbol whenever possible, so changing `ai-char` does not require relearning from scratch.
- `state.json` stores only pending transition data; `qtable.json` stores learned transition quality.
- Configuration, pending-move state, and learned transition quality have separate lifecycles and remain separate persisted concepts.
- Persisted learning data must remain independent from incidental process state.
- The CLI writes exactly one machine-readable JSON result to standard output: a move coordinate object or `null` when no legal move exists. Human-readable diagnostics belong on standard error.
