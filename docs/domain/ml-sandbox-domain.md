# ML Sandbox Domains

| Area | Scope |
| --- | --- |
| `nn/` | Perceptron and feed-forward neural networks |
| `knn/` | Distance metrics, neighbour voting, weighting and charting |
| `TF/` | TensorFlow/GPU checks and network prototypes |
| `scratch/` | Small algorithm explorations and quick checks |

| Term | Meaning |
| --- | --- |
| Experiment | Local algorithm exploration without production packaging guarantees. |
| Prototype | Trial implementation before any deliberate production adoption. |
| Dataset | Input interpreted under the experiment's assumptions. |
| Smoke check | Quick run confirming the expected input shape still works. |

Experiments test ideas with local datasets and assumptions. Reproducible results identify the dataset, dependency versions, parameters and sources of randomness. Prototype behaviour becomes a production contract only through deliberate adoption. Prioritize algorithmic correctness, clarity and reproducibility; document non-obvious inputs near the code. Keep abstractions local until sharing solves a concrete problem. Production extraction belongs in `games_theory/` and its [domain documentation](games-theory-domain.md).
