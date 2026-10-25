# INBOX

- [ ] Prevent learning across round resets: discard stale pending moves when boards are discontinuous (>1 changed cell, size mismatch or malformed state); scores may remain cumulative.
- [ ] Add a board-free `game-over` Python/CLI operation with final scores; apply terminal reward with zero future value, propagate over persisted episode history, then clear the episode. Preserve existing move calls and load old state files without history. Cover continuity, resets, history, terminal learning and CLI compatibility with regression tests.
- [ ] Research Q-learning training strategies: explain the current loop and credit assignment, compare automated opponents/self-play, exploration, terminal propagation, trajectory storage and symmetry; recommend incremental experiments with measurable outcomes. Keep explicit game-over propagation separate from silent reset cleanup.
