# Engineering Guide

This guide defines how NeuralNetworks code should be designed, implemented, and tested.

## Application Structure

- Keep the CLI and other entry points responsible for input parsing, dependency construction, and top-level workflow selection.
- Keep game rules, state encoding, learning policy, and move selection independent of CLI parsing and filesystem formats.
- Put lifecycle and mode decisions in the top-level orchestrator; lower-level services should expose explicit operations instead of boolean switches that alter persistence or side effects.
- Isolate configuration, state, and Q-table persistence behind repositories with clear ownership of each resource.
- Inject configuration, randomness, and persistence collaborators when business logic needs them; do not construct external dependencies deep inside domain logic.
- Prefer small components with one reason to change over broad classes that combine policy, orchestration, and persistence.
- Keep experimental code lightweight and local to the experiment until a repeated need justifies extraction.

## Domain Types And State

- Represent board state, points, pending moves, configuration, Q-table entries, and public move coordinates with explicit types.
- Normalize external `X`, `O`, and `N` symbols at the application boundary; learning logic should operate on bot-relative canonical state.
- Keep row-major indexing and zero-based public coordinates explicit at conversion boundaries.
- Validate state transitions before deriving a move or applying a learning update.
- Keep persistent resource schemas independent from incidental in-memory implementation details.
- Treat absent state, malformed state, and a valid empty state as different conditions.

## Error Handling And Public Interfaces

- Validate CLI arguments and configuration before starting prediction or mutating persisted state.
- Return contextual errors from parsing, validation, persistence, state encoding, and prediction paths.
- Do not silently recover from malformed configuration or persisted learning data when doing so could overwrite user state.
- Write only the documented machine-readable result to standard output; send diagnostics to standard error.
- Keep public CLI behavior and importable APIs backward-compatible unless an intentional contract change includes migration and regression coverage.
- Make initialization, overwrite, reset, read-only, and learning operations explicit rather than inferring them from ambiguous flags.

## Persistence And Side Effects

- Use the owning repository or resource service for reads and writes instead of accessing JSON files from orchestration or policy code.
- Keep configuration, pending-move state, and learned Q-values in separate resources because they have different lifecycles.
- Persist related state changes in a deliberate order and avoid leaving partially updated resources after a failure.
- Do not overwrite user resources outside an explicit initialization or reset operation.
- Keep reusable package code independent of the repository checkout and current working directory.
- Make randomness an explicit policy dependency when deterministic behavior is needed for tests.

## Anti-patterns

- Do not read/write `config.json`, `state.json`, or `qtable.json` directly from orchestration code when a repository/service exists.
- Do not duplicate current state across multiple resource files unless the lifecycle is intentionally different and documented.
- Do not make Q-table semantics depend on external symbols (`X`/`O`) when canonical bot-relative state is available.
- Do not silently overwrite user resources outside explicit init/reset workflows.
- Do not hide write/read-only mode changes behind generic boolean flags inside lower-level services; split the operation and let the orchestrator choose.

## Testing

- Unit-test state normalization, neighbour generation, Q-value updates, reward calculation, transition validation, and coordinate derivation.
- Cover malformed inputs, incompatible resource data, missing files, empty legal-move sets, and persistence failures.
- Use temporary resources and injected collaborators instead of modifying packaged defaults or user data in tests.
- Keep tests deterministic by controlling randomness and filesystem state.
- Add a regression test for every corrected prediction, persistence, or public-interface bug.
- Test experiments at the level needed to protect their algorithmic result without imposing production structure that provides no concrete benefit.

## Code Review Standard

- Focus on correctness, behavioural regressions, user-data loss, persistence safety, public contract changes, and missing tests.
- Make findings actionable by explaining the impact and pointing to specific files and lines.
- Avoid cosmetic findings unless they hide a functional problem or make domain or persistence semantics unclear.
- Verify that abstractions reduce coupling without hiding game rules, learning semantics, or side effects.
- Require tests for changed parsing, state transitions, learning policy, persistence, and failure handling.
- For experimental code, prioritize algorithmic correctness and clarity; require additional structure only when a concrete risk justifies it.
