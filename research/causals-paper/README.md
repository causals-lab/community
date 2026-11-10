# Causals snapshot analysis

Reproducible structural measurements for Causals v0.1.0-2026-10-09.
The analysis covers the complete public snapshot: 369,184 nodes and
1,272,418 edges. It reports file integrity, labels and relations, source-record
coverage, timestamp formatting, connectivity, and deterministic multi-hop
reachability. The graph contains contextual relationships and attributed causal
claims; the measurements do not estimate semantic accuracy.

## Run

Requires Python 3.10 or later and only the standard library. From this repository:

```bash
python3 research/causals-paper/audit_snapshot.py \
  data/v0.1.0-2026-10-09 \
  /tmp/causals_snapshot_audit.json
```

The release directory must contain `nodes.jsonl.gz`, `edges.jsonl.gz`, and
`manifest.json`. Full-file analysis holds graph indices in memory and can take
several gigabytes of RAM. It reads the supplied files and writes one aggregate
JSON file. It does not connect to a database or call a model.

## Files and interpretation

- `audit_snapshot.py`: complete analysis program.
- `snapshot_audit.json`: the results used in the manuscript, including input
  SHA-256 hashes and release version.
- `LICENSE_CODE`: MIT license for this analysis program only.

For reachability, eligible seeds have the Entity label, lack the Event label,
and have an outgoing RELATES_TO edge. Sorting their IDs by SHA-256 digest
selects the first 100. Outgoing breadth-first traversal counts distinct other
nodes cumulatively within one, two, and three hops. No semantic or temporal
filter is applied. Mean counts are 13.20, 430.72, and 4,424.65; medians are
1, 20, and 1,255. These are graph-size measurements, not affected-entity labels
or measures of causal reasoning depth.

Repeat runs should reproduce aggregate measurements for the same compressed
input files. `audit_date_utc` and `elapsed_seconds` vary by execution. The elapsed
time is recorded for the run and is not a performance benchmark.

The graph data and aggregate results use the snapshot's
[CC BY 4.0 terms](../../data/v0.1.0-2026-10-09/LICENSE_DATA.md).
The MIT grant applies only to `audit_snapshot.py`; it grants no rights to the
private graph-building or inference software.

Please report corrections through repository issues. Private data concerns can
be sent to **data@causals.org**. See [CONTRIBUTING.md](../../CONTRIBUTING.md).
