# Production Package Guide

This guide defines the production quality standard for the `games-theory` package.

## Scope And Priorities

- The installable package, CLI entry points, packaged defaults, persistence formats, and public Python interfaces form one production surface.
- The package may be published independently and must not depend on the repository checkout at runtime.
- Public interfaces and resource formats remain backward-compatible unless an explicit migration path and regression coverage are provided.
- Packaged defaults must be valid, internally consistent, and safe to copy into a new environment.

## Packaging And Release Checklist

- Package metadata matches the current version, entry points, runtime dependencies, and supported Python version.
- `flit build` or `pip install .` succeeds without missing package files/resources when release work is in scope.
- A release dependency lock is generated from the built wheel metadata, contains the complete hashed runtime dependency closure, and installs successfully before the release is published.

## Runtime And CLI Checklist

- `games-theory` validates inputs, loads configs, and triggers predictor flow without regressions.
- `games-theory-init` copies defaults, honours `--overwrite`, and regenerates internals only when requested.
- Resource helpers avoid corrupting or silently overwriting user data.

## Predictor And Persistence Checklist

- Predictor, generator, repository, and policy changes preserve state compatibility and include regression coverage.
- `qtable.json` and `state.json` changes preserve their domain meaning or provide an explicit migration.
- Predictor and persistence failures must not leave user resources silently corrupted or partially reset.

## Test Checklist

- Unit tests cover changed production logic, public contracts, and failure handling.
- CLI and integration smoke checks cover installability, packaged resources, initialization, and prediction output.
- The complete verification workflow must build the package from its declared metadata rather than relying only on editable imports.
