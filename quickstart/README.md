# Causals Graph quickstart

Run the [10-minute notebook](quickstart.ipynb) to inspect a small, real extract from the fixed [v0.1.0-2026-10-09 release](../data/v0.1.0-2026-10-09/). It needs Python 3 and its standard library, but no NewsGraph installation, database, API key, or GPU.

To run locally, download or clone this repository, open `quickstart/quickstart.ipynb` in any Python notebook environment, and run its cells in order. [Open it in Google Colab](https://colab.research.google.com/github/causals-lab/community/blob/main/quickstart/quickstart.ipynb) if you prefer not to set up Python locally. Colab downloads the three small files in [`sample/`](sample/) from this public repository; each request has a 15-second timeout. The notebook verifies their SHA-256 checksums before using them.

The sample includes 62 nodes and 9 directed edges selected from three examples on the [Graph page](https://causals.org/graph.html): a Red Sea route, several Federal Reserve links, and Black Sea wheat shipping. It includes every edge endpoint and referenced source-news node, so the joins can be checked without the full download. It deliberately excludes Person nodes. The sample is **selected for teaching, not representative**, and its edges have **not** been independently verified as causal effects. Source-news IDs do not provide article text or URLs in this release.

The notebook demonstrates how to check files, join `source_id` and `target_id` to node `id`, inspect neighborhood relations, and see what the released provenance can and cannot establish. Next, use the [full snapshot](../data/v0.1.0-2026-10-09/) or [Hugging Face mirror](https://huggingface.co/datasets/causals-lab/causals-graph). Read the [data card](../data/v0.1.0-2026-10-09/DATA_CARD.md) before drawing conclusions.

The sample data is part of the Causals Graph v0.1.0-2026-10-09 release, offered under [CC BY 4.0](../data/v0.1.0-2026-10-09/LICENSE_DATA.md). Attribute **Causals Lab**, identify the version, link to the release and license, and indicate changes. This data license is not a blanket license for code or third-party news content.

To regenerate the sample from the full released files, run `python3 quickstart/build_sample.py` from the repository root. It reads only the public compressed JSONL files, selects the nine listed edge IDs plus all their referenced nodes, and rewrites `sample/` deterministically. The sample manifest records the source-release manifest hash, selection, counts, and file hashes.
