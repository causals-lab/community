# Causals Graph v0.1.0-2026-10-09

This is a versioned, news-derived **graph snapshot**, not a database of
independently verified causal effects. It includes entities, events,
source-news records, and directed relationships. The separate inference
rulebook and per-run inference ledger are not included.

## Files and size

- `nodes.jsonl.gz`: 369,184 nodes, one UTF-8 JSON object per line, gzip-compressed.
- `edges.jsonl.gz`: 1,272,418 edges in the same format.
- `manifest.json`: file hashes, counts, relation distribution, and version.
- `LICENSE_DATA.md`: reuse terms for the released dataset.

The source graph export was generated on 2026-10-09T01:11:38.694801+00:00.
This release was packaged separately; it is a snapshot, not a live feed.

## Schema

Node fields: `id`, `labels`, `kind`, and optionally `name`, `valid_at`,
`published_at`, `symbol`. An ID identifies a node within this snapshot; ID
stability across later rebuilds and entity merges has not been established.
`Event` and `Episodic` node names are omitted.

Edge fields: `id`, `source_id`, `target_id`, `type`, `relation`,
`source_episode_ids`, and optionally `valid_at`, `invalid_at`, `as_of`.
`source_id` and `target_id` join to node `id`. Every
`source_episode_ids` entry joins to an included `Episodic` node. It is a
source-news *identifier*, not article text or a URL. Edge direction describes
the stored relation; it is not necessarily the direction in which the private
inference engine propagates state.

For `RELATES_TO` edges, `relation` is the controlled code stored in the
source graph's relationship `name` field. For `MENTIONS` and `VARIANT_OF`,
`relation` equals the relationship type. The 41 observed
relation values in this snapshot are not a claim that every value is in the
current canonical ontology.

## Interpretation and quality limits

The snapshot contains 703,361 `MENTIONS`,
529,414 `RELATES_TO`, and
39,643 `VARIANT_OF` edges. Many links are descriptive or contextual, not causal.
`OTHER` means unclassified. `SHIFTED` records an observation and is not a
causal mechanism. `TRIGGERED` and `STATED_CAUSE` are extracted or attributed
causal claims, not independent proof that an intervention would have an
effect. Graph paths must not be treated automatically as causal paths.

Of 8,231 `TRIGGERED` edges,
1,223 have no released source-news ID. Also,
650 `TRIGGERED` and
169 `STATED_CAUSE` edges do not join two Event-labeled
nodes. These counts are quality cautions, not an estimated error rate. There
has been no representative whole-graph accuracy or causal-validity study.
Users should define and inspect the subset used for a research claim.

The publication filter excluded 82,921 `Person` nodes
and their incident edges, plus 583
non-Person nodes with names matching excluded people. This is a conservative
filter, not a guarantee that retained entities are perfectly classified.
News headlines, article text, event names, article URLs, publisher text,
edge free-text facts, `original_name`, prompts, and model scores are not
included. Without article URLs, the package alone does not support direct
external inspection of source articles.

Automated checks passed for hashes, unique IDs, record counts, endpoint
references, source-news references, allowed fields, and relation totals.
They do **not** establish factual correctness, comprehensive privacy
protection, or that any particular edge is causal.

## Reuse, citation, and corrections

The released dataset is offered under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); attribute
**Causals Lab**, identify this version, link to the release and license,
and indicate changes. The license applies only to rights the publisher can
grant in these released files. It does not license third-party news content,
trademarks, privacy/publicity rights, the private inference system, or the
website's source code. No warranty of correctness is given.

Suggested citation until a persistent DOI is available:

> Causals Lab. (2026). *Causals Graph* (v0.1.0-2026-10-09) [Data set].
> https://github.com/causals-lab/community/tree/graph-v0.1.0-2026-10-09/data/v0.1.0-2026-10-09

Report data corrections or removal concerns privately to **data@causals.org**.
Do not post personal or sensitive details in a public GitHub issue.

## Verify a download

Compare the SHA-256 digest of each `.gz` file with `manifest.json`. For
example, on macOS/Linux: `shasum -a 256 nodes.jsonl.gz edges.jsonl.gz`.
Use a streaming JSONL reader; loading all records into memory is optional.
