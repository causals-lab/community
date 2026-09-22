# Causals Lab

**Causals Lab** is building an evidence-backed, versioned map of causal claims and related relationships, and studying how graphs and language models can reason together.

Our public work has four parts:

- **Causals Graph** — a navigable knowledge graph. A recorded causal claim is not, by itself, proof of causation.
- **Causals Ontology** — definitions for entities, relationships, evidence, uncertainty, and provenance.
- **Causals Bench** — evaluation tasks and datasets for graph-and-LLM reasoning.
- **Causals Commons** — the community that proposes, checks, and improves this work.

Website: [causals.org](https://causals.org) (launch in progress).

## Contribute

You can report a missing or incorrect node or relationship, supply a verifiable source, challenge a causal interpretation, review a proposal, or help design an evaluation task. Start with [CONTRIBUTING.md](CONTRIBUTING.md). You do not need to know Git to report a graph issue.

Every accepted graph change should be traceable to a proposal, evidence, a review decision, and a graph version. Human and LLM-generated proposals go through review before publication.

**Never post an LLM API key or other credential** in an issue, discussion, pull request, or graph submission.

## What is open today?

This repository is a public collaboration space. Public visibility does not grant permission to reuse graph data, benchmark material, or implementation code. The release scope and licenses for each are being decided separately; see [OPENNESS.md](OPENNESS.md). The graph-building implementation is not part of this public repository.

Moirai is a separate commercial application. The Lab's public research, data-release decisions, and contribution rules are described here rather than inferred from the app.

## Important distinction

The graph may record a proposed mechanism, an observed association, an intervention result, or a disputed claim. These are different kinds of knowledge and must not be presented as equally established causal effects. Sources, time context, uncertainty, and disagreements matter.
