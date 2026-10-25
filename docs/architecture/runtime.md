# Q-learning Runtime

One CLI invocation observes a board and returns one bot move. The caller owns the game loop and sends the updated board and scores on the next invocation. Learning therefore evaluates the saved transition after the opponent has moved.

```mermaid
flowchart TD
    A["CLI: scores, row-major board, config path"] --> B["Load config; validate board length<br/>StateEncoder: X/O/N → bot-relative state S"]
    B --> C{Learning enabled?}
    C -->|Yes| D["Load state.json"]
    D --> E{"Usable pending last_move?<br/>Saved from/to present?"}
    E -->|Yes| F["Load Q-table; ensure entries<br/>for previous state and current S"]
    F --> G["R = current advantage − saved advantage<br/>Future = max Q from S, or 0 if none"]
    G --> H["Q_prev ← Q_prev + α × (R + γ × Future − Q_prev)"]
    H --> I["Save Q-table, then clear last_move"]
    E -->|No| J["Skip deferred update"]
    I --> K["Load Q-table; generate legal neighbours of S<br/>Register missing transitions with value 0"]
    J --> K
    K --> L{Any legal neighbours?}
    L -->|Yes| M["Select next state using Q-value weights<br/>Equal values → uniform random"]
    M --> N["Save last_move: from, to, points, advantage<br/>Then save Q-table"]
    L -->|No| O["Save last_move = null<br/>Then save Q-table"]
    C -->|No| P["Load Q-table; use known neighbours<br/>or generate candidates in memory"]
    P --> Q["Select using the same policy<br/>No writes to state or Q-table"]
    N --> T{Move selected?}
    O --> T
    Q --> T
    T -->|Yes| U["Validate selected transition<br/>Derive zero-based x, y from changed cell"]
    U --> V["stdout: JSON coordinate"]
    T -->|No| W["stdout: JSON null"]
    V --> X["Diagnostics → stderr; invocation ends"]
    W --> X
```

| Component (`games_theory/`) | Responsibility |
| --- | --- |
| `process.py` | CLI validation, learning/read-only routing and JSON output |
| `src/config_repository.py` | Load runtime configuration |
| `src/default_predictor.py` | Evaluate the previous move and predict the next one |
| `src/domain_types.py` | Shared board, score, configuration, pending-move, Q-table and coordinate contracts |
| `src/predictor/` | StateEncoder, StateRepository, QTableRepository, RewardPolicy, ScoreTracker and ActionSelector |
| `src/generator.py` | Generate candidate bot moves |
| `src/move_coordinate_deriver.py` | Convert a selected transition into `{x, y}` |
| `resources/resource.py` | Initialize resources and provide file utilities |

| Resource under `DIR/data/` | Owner / contents |
| --- | --- |
| `config.json` | ConfigRepository: board size, bot symbol, learning flag |
| `state.json` | StateRepository: pending `last_move` (`from`, `to`, `points`, `advantage`) |
| `qtable.json` | QTableRepository: canonical-state → next-state → value; initialized empty and populated lazily |

`Q ← Q + α × (reward + γ × max_future_Q − Q)`, with default `α = 0.1`, `γ = 0.5`. Reward is the change in bot score advantage. Equal action values use uniform random selection; otherwise selection is weighted, shifting nonpositive values to positive weights.

The Q-table and pending state are separate JSON writes, not one transaction. Missing files load as an empty Q-table or no pending move; malformed JSON propagates an error. Read-only prediction does not write resources. Round-boundary detection, episode history and explicit terminal learning are future work in [INBOX](../../INBOX.md).
