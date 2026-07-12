# CLI Move Coordinate Output

## Status
- Phase: Awaiting Acceptance

## Scope
- Change the `games-theory` CLI result to emit exactly one JSON value on standard output: `{"x": <column>, "y": <row>}` for the selected move or `null` when no legal move is available.
- Define coordinates as zero-based, with `(0, 0)` at the top-left, `x` increasing to the right, and `y` increasing downward.
- Derive the coordinate from the single changed cell between the current canonical board state and the state selected by `DefaultPredictor`.
- Keep diagnostics, including the current board and Q-table, on standard error so integrations can parse standard output without filtering logs.
- Preserve the existing Q-learning, action-selection, and persistence behaviour.
- Keep target-application integrations out of scope.

## Implementation Plan
1. [done] Add a typed move-coordinate contract and a small conversion function that validates the selected transition and maps its row-major cell index to `(x, y)` using the configured board size.
2. [done] Make `Process.move()` return the optional coordinate while preserving the current learning and read-only predictor paths.
3. [done] Serialize the returned coordinate once at the CLI boundary with `json.dumps`, producing one JSON value on standard output; retain diagnostic output on standard error.
4. [done] Add unit tests for corner/interior coordinates, no available move, malformed transitions, learning-disabled behaviour, and separation of machine-readable standard output from diagnostics.
5. [done] Document the public JSON output, coordinate system, and `null` result in the domain and repository guide; update the runtime-flow diagram if the implementation introduces a material flow change.

## Verification
- `python3 -m unittest discover -s games_theory/test -p 'test_*.py'`
- `bash scripts/verify.sh`
- Run a CLI smoke invocation against temporary initialized resources and verify that standard output is valid JSON while diagnostics are written only to standard error.

## Result
- The CLI emits one JSON move coordinate or `null` on standard output while retaining diagnostics on standard error.
- Transition validation, process behaviour, CLI serialization, and the no-move case are covered by 27 passing tests.
- The process test uses a single configured Q-table transition and asserts one exact coordinate, avoiding an ambiguous collection of possible random results.
- `bash scripts/verify.sh` and a source-level CLI smoke test passed; the smoke output was valid JSON and diagnostics were isolated on standard error.
