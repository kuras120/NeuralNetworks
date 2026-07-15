# Machine Learning Sandbox Domain

This file describes the exploratory machine-learning sandbox domain. Use it before changing experiment structure, datasets, prototype scripts, or research workflows outside the production `games_theory/**` package.

## Bounded Context

| Context | Code paths | Responsibility |
| --- | --- | --- |
| Neural Network Experiments | `nn/**`, `nn/nn_main.py` | Prototype perceptron and feed-forward neural-network behaviour. |
| k-NN Experiments | `knn/**`, `knn_main.py` | Explore distance metrics, neighbor voting, weighting, and charting. |
| TensorFlow Prototypes | `TF/**` | Validate TensorFlow/GPU setup and prototype network definitions. |
| Scratch Space | `scratch/**`, `data/**` | Hold quick checks, sample data, and disposable algorithm explorations. |

## Ubiquitous Language

- **Experiment**: localized code used to test an algorithmic idea without production packaging guarantees.
- **Prototype**: implementation intended for learning or validation before any production extraction.
- **Dataset**: local input data used by experiments; changes should be documented when they affect reproducibility.
- **Smoke check**: lightweight command that proves a prototype still runs for its expected input shape.

## Domain Rules

- Optimize sandbox changes for correctness, clarity, and research velocity.
- Keep experiment-specific abstractions local until there is a repeated, concrete need to share them.
- Do not impose production package structure on experiments unless it fixes a real maintenance or correctness problem.
- Document non-obvious experiment assumptions near the experiment or in this domain file.
- If sandbox work graduates into production behaviour, move the durable domain language into the relevant production domain docs.
