# Game Theory Domain

This file describes the production game-theory domain from a DDD perspective. Use it before changing Q-learning behaviour, naming, persistence contracts, or public workflows in `games_theory/**`.

## Bounded Contexts

| Context | Code paths | Responsibility |
| --- | --- | --- |
| Game Theory Runtime | `games_theory/**` | Runs the turn-based Q-learning backend, persists learning state, and exposes CLI entry points. |

## Game Theory Ubiquitous Language

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
- Resource format changes are production changes and require tests plus documentation updates.
- The CLI writes exactly one machine-readable JSON result to standard output: a move coordinate object or `null` when no legal move exists. Human-readable diagnostics belong on standard error.
