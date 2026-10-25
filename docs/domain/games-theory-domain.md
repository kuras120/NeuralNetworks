# Game Theory Domain

Scope: `games_theory/` provides a turn-based Q-learning backend. The caller owns game rules, turn progression and scoring.

| Responsibility | Boundary |
| --- | --- |
| Game interface | Receive board/scores and return a public move coordinate. |
| State normalization | Translate external symbols using `ai-char` at the application boundary. |
| Learning | Evaluate the previous transition, maintain Q-values and select the next action. |
| Persistence | Carry configuration, pending moves and learned values across invocations. |

| Term | Meaning |
| --- | --- |
| Board | Row-major external cells: `X`, `O`, `N` (empty). `X` starts; the bot may use either marker. |
| Canonical state | Bot-relative cells: `-1` bot, `1` opponent, `0` empty; independent of the external bot symbol. |
| Neighbour | Candidate next state formed by placing one bot marker in an empty cell. |
| Move coordinate | Zero-based `{x, y}`; origin at top-left, x rightward, y downward. |
| Q-table | Stored transition values keyed by canonical state and candidate next state. |
| Last move | Saved bot transition, evaluated on the next learning invocation after the opponent move. |
| Reward | Change in bot advantage (`ai_points − player_points`) since the pending move. |

Configuration, pending transition and learned Q-values have independent lifecycles and separate resources. Persisted learning data is independent of incidental process state. Changing `ai-char` preserves the meaning of canonical Q-values and does not require relearning from scratch. Resource format changes need compatibility handling and regression tests. The CLI emits one JSON move or `null` on stdout; diagnostics use stderr.

See [runtime and persistence](../architecture/runtime.md) and [planned work](../../INBOX.md).
