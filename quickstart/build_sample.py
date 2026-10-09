"""Build the small, reproducible teaching sample from the public v0.1.0 snapshot.

The chosen edges are the three examples displayed at causals.org/graph.html.
This script requires only Python's standard library and the released files in
../data/v0.1.0-2026-10-09/. It never reads the private NewsGraph database.
"""

from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path


VERSION = "v0.1.0-2026-10-09"
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / VERSION
OUTPUT = Path(__file__).resolve().parent / "sample"

EDGE_IDS = {
    # Red Sea: a conflict actor, a shipping route, and a market index.
    "fffb338f-57ae-4566-acc9-e4edffdf79e8",
    "68c24879-a541-43db-8b05-763e2af812ea",
    "d3b69d5d-f179-455c-b2f0-20a3063b1d40",
    # Federal Reserve: three different target types.
    "93d65c52-069b-4cb6-9117-1a6901948f5a",
    "9dae5ed8-668e-4336-a474-f8bfa2c0888e",
    "7c4b0a35-d9db-4f1b-8c25-8bfa52837b0e",
    # Black Sea: two producers, a commodity, and a route.
    "6045b66b-d86f-4227-a4d8-0a716afb6492",
    "95717613-d400-4871-ae2f-4f940f1b4172",
    "998c7b77-51da-44eb-b7c2-d787fcf60e0b",
}


def read_jsonl_gz(path: Path):
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            yield json.loads(line)


def write_jsonl(path: Path, records: list[dict]) -> dict:
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for record in sorted(records, key=lambda item: item["id"]):
            stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")
    return {
        "file": path.name,
        "records": len(records),
        "bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def main() -> None:
    edges = [edge for edge in read_jsonl_gz(SOURCE / "edges.jsonl.gz") if edge["id"] in EDGE_IDS]
    if {edge["id"] for edge in edges} != EDGE_IDS:
        raise ValueError("One or more chosen edge IDs are absent from the released snapshot")
    if any(edge.get("invalid_at") for edge in edges):
        raise ValueError("A chosen edge has an invalid_at value; review the sample selection")

    endpoint_ids = {node_id for edge in edges for node_id in (edge["source_id"], edge["target_id"])}
    source_news_ids = {node_id for edge in edges for node_id in edge.get("source_episode_ids", [])}
    wanted_ids = endpoint_ids | source_news_ids
    nodes = [node for node in read_jsonl_gz(SOURCE / "nodes.jsonl.gz") if node["id"] in wanted_ids]
    if {node["id"] for node in nodes} != wanted_ids:
        raise ValueError("The sample would contain an edge with a missing endpoint or source-news node")
    if any("Person" in node.get("labels", []) for node in nodes):
        raise ValueError("A Person node appeared in the sample")

    OUTPUT.mkdir(exist_ok=True)
    files = [write_jsonl(OUTPUT / "nodes.jsonl", nodes), write_jsonl(OUTPUT / "edges.jsonl", edges)]
    manifest = {
        "schema": "causals-graph-quickstart/1",
        "source_snapshot": VERSION,
        "source_manifest_sha256": hashlib.sha256((SOURCE / "manifest.json").read_bytes()).hexdigest(),
        "selection": "Nine specific edges from the three examples on causals.org/graph.html, with every endpoint and referenced source-news node",
        "edge_ids": sorted(EDGE_IDS),
        "endpoint_nodes": len(endpoint_ids),
        "source_news_nodes": len(source_news_ids),
        "files": files,
        "license": "CC BY 4.0; attribute Causals Lab and the source snapshot",
        "interpretation": "A teaching sample of graph records, not a representative or independently validated set of causal effects",
    }
    (OUTPUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Built {len(nodes)} nodes and {len(edges)} edges in {OUTPUT}")


if __name__ == "__main__":
    main()
