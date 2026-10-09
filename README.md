# Causals Lab

**Causals Lab** is building an evidence-backed, versioned map of causal claims and related relationships, and studying how graphs and language models can reason together.

Our public work has four parts:

- **Causals Graph** — a navigable knowledge graph. A recorded causal claim is not, by itself, proof of causation.
- **Causals Ontology** — definitions for entities, relationships, evidence, uncertainty, and provenance.
- **Causals Bench** — evaluation tasks and datasets for graph-and-LLM reasoning.
- **Causals Commons** — the community that proposes, checks, and improves this work.

Website: [causals.org](https://causals.org).

## Download the graph

The first public graph snapshot is [Causals Graph v0.1.0-2026-10-09](data/v0.1.0-2026-10-09/). It contains 369,184 nodes and 1,272,418 directed edges. The [data card](data/v0.1.0-2026-10-09/DATA_CARD.md) explains the fields, source limitations, and why a recorded relationship is not proof of causation. The dataset is offered under [CC BY 4.0](data/v0.1.0-2026-10-09/LICENSE_DATA.md); software and third-party news content are not included in that grant. For private correction or removal requests, write to **data@causals.org**.

## Contribute

You can report a missing or incorrect node or relationship, supply a verifiable source, challenge a causal interpretation, review a proposal, or help design an evaluation task. Start with [CONTRIBUTING.md](CONTRIBUTING.md). You do not need to know Git to report a graph issue.

Every accepted graph change should be traceable to a proposal, evidence, a review decision, and a graph version. Human and LLM-generated proposals go through review before publication.

## What is open today?

This repository is a public collaboration space. The **versioned graph snapshot** above has explicit CC BY 4.0 terms. Public visibility alone does not grant permission to reuse other graph versions, benchmark material, or implementation code; see [OPENNESS.md](OPENNESS.md). The graph-building implementation is not part of this public repository.

Moirai is a separate commercial application. The Lab's public research, data-release decisions, and contribution rules are described here rather than inferred from the app.

## Important distinction

The graph may record a proposed mechanism, an observed association, an intervention result, or a disputed claim. These are different kinds of knowledge and must not be presented as equally established causal effects. Sources, time context, uncertainty, and disagreements matter.
