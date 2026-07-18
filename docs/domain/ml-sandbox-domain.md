# Machine Learning Sandbox Domain

This document defines the purpose, language, and boundaries of the exploratory machine-learning sandboxes.

## Bounded Context

| Context | Responsibility |
| --- | --- |
| Neural Network Experiments | Prototype perceptron and feed-forward neural-network behaviour. |
| k-NN Experiments | Explore distance metrics, neighbour voting, weighting, and charting. |
| TensorFlow Prototypes | Validate TensorFlow/GPU setup and prototype network definitions. |
| Scratch Space | Hold quick checks, sample data, and disposable algorithm explorations. |

## Ubiquitous Language

- **Experiment**: localized code used to test an algorithmic idea without production packaging guarantees.
- **Prototype**: implementation intended for learning or validation before any production extraction.
- **Dataset**: input data used by an experiment and interpreted under that experiment's assumptions.
- **Smoke check**: lightweight command that proves a prototype still runs for its expected input shape.

## Domain Rules

- Sandboxes optimize for correctness, clarity, and research velocity rather than packaging guarantees.
- Keep experiment-specific abstractions local until there is a repeated, concrete need to share them.
- Do not impose production package structure on experiments unless it fixes a real maintenance or correctness problem.
- Reproducible results identify the relevant dataset, dependency versions, parameters, and sources of randomness.
- Prototype behavior is not a production contract until it is deliberately adopted by a production domain.
