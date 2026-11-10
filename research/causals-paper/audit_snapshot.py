"""Reproduce aggregate-only analyses of the released Causals snapshot.

No database connection, model calls, source-text export, or mutations of inputs.
Usage: python3 research/causals_paper/audit_snapshot.py RELEASE_DIR OUTPUT_JSON
"""
import argparse
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import statistics
import time


def rows(path):
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        for line in f:
            yield json.loads(line)


class Components:
    def __init__(self, n):
        self.p = list(range(n))
        self.s = [1]*n

    def root(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def add(self, a, b):
        a, b = self.root(a), self.root(b)
        if a == b:
            return
        if self.s[a] < self.s[b]:
            a, b = b, a
        self.p[b] = a
        self.s[a] += self.s[b]

    def summary(self, active):
        c = Counter(self.root(i) for i in active)
        sizes = sorted(c.values(), reverse=True)
        return {'nodes': len(active), 'weak_components': len(sizes),
                'largest_component_nodes': sizes[0] if sizes else 0,
                'isolates_in_node_universe': sum(v == 1 for v in sizes)}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('release', type=Path)
    ap.add_argument('output', type=Path)
    args = ap.parse_args()
    start = time.monotonic()
    manifest = json.loads((args.release/'manifest.json').read_text())
    checks = {}
    for spec in manifest['files']:
        path = args.release/spec['file']
        h = hashlib.sha256()
        with path.open('rb') as f:
            for block in iter(lambda: f.read(1024*1024), b''):
                h.update(block)
        checks[spec['file']] = {'sha256': h.hexdigest(), 'bytes': path.stat().st_size,
            'matches_manifest': h.hexdigest() == spec['sha256'] and path.stat().st_size == spec['bytes']}
    ids, labs, kinds, node_fields, dates = {}, [], Counter(), Counter(), defaultdict(list)
    labels, date_bad, date_present, date_types = Counter(), Counter(), Counter(), Counter()
    name_count, duplicate_nodes = 0, 0
    allowed_n = {'id','labels','kind','name','valid_at','published_at','symbol'}
    allowed_e = {'id','source_id','target_id','type','relation','source_episode_ids','valid_at','invalid_at','as_of'}
    unexpected_n, unexpected_e = Counter(), Counter()

    def check_dates(row, prefix):
        for field in ('valid_at','published_at','invalid_at','as_of'):
            val = row.get(field)
            if val is None or val == '':
                continue
            key = prefix+'.'+field
            date_present[key] += 1
            date_types[key+'.'+type(val).__name__] += 1
            try:
                d = datetime.fromisoformat(str(val).replace('Z','+00:00'))
                if d.tzinfo is None:
                    date_bad[key+'.naive'] += 1
                dates[key].append(d.isoformat())
            except (ValueError, TypeError):
                date_bad[key+'.unparseable'] += 1

    for node in rows(args.release/'nodes.jsonl.gz'):
        duplicate_nodes += node['id'] in ids
        ids[node['id']] = len(labs)
        ls = set(node['labels']); labs.append(ls)
        kinds[node.get('kind','<missing>')] += 1
        labels.update(ls); node_fields.update(node.keys())
        unexpected_n.update(set(node)-allowed_n)
        name_count += bool(node.get('name'))
        check_dates(node, 'node')
    n = len(labs)
    full, semantic, claims = Components(n), Components(n), Components(n)
    active_s, active_c, degree = set(), set(), Counter()
    relations, types, edge_fields, sourced, selfloops = Counter(), Counter(), Counter(), Counter(), Counter()
    claim_issues = Counter(); edge_ids = set(); triples = set(); adjacency = defaultdict(set)
    issues = Counter(); source_sizes = Counter(); rel_dated = Counter()
    for edge in rows(args.release/'edges.jsonl.gz'):
        issues['duplicate_edge_ids'] += edge['id'] in edge_ids
        edge_ids.add(edge['id'])
        unexpected_e.update(set(edge)-allowed_e)
        rel, typ = edge['relation'], edge['type']
        relations[rel] += 1; types[typ] += 1; edge_fields.update(edge.keys())
        sources = edge.get('source_episode_ids', [])
        sourced[rel] += bool(sources); source_sizes[len(sources)] += 1
        issues['duplicate_sources_within_edge'] += len(sources)-len(set(sources))
        for source in sources:
            issues['missing_or_non_episode_source_ids'] += source not in ids or 'Episodic' not in labs[ids[source]]
        if edge['source_id'] not in ids or edge['target_id'] not in ids:
            issues['dangling_endpoints'] += 1
            continue
        a, b = ids[edge['source_id']], ids[edge['target_id']]
        full.add(a,b); degree[a] += 1; degree[b] += 1
        selfloops[rel] += a == b
        key = (a,b,rel)
        issues['repeated_source_target_relation_records'] += key in triples
        triples.add(key)
        if typ == 'RELATES_TO':
            semantic.add(a,b); active_s.update((a,b)); adjacency[a].add(b)
            if sources:
                issues['sourced_semantic_edges'] += 1
        if rel in {'TRIGGERED','STATED_CAUSE'}:
            claims.add(a,b); active_c.update((a,b))
            claim_issues[rel+'.without_source'] += not bool(sources)
            claim_issues[rel+'.non_event_pair'] += not ('Event' in labs[a] and 'Event' in labs[b])
            claim_issues[rel+'.self_loop'] += a == b
        rel_dated[rel] += any(edge.get(k) not in (None,'') for k in ('valid_at','invalid_at','as_of'))
        check_dates(edge, 'edge')

    # Deterministic sample of non-Event Entity-labelled nodes. These are structural
    # reachability measurements, never causal-effect predictions.
    candidates = [(hashlib.sha256(k.encode()).digest(), i) for k,i in ids.items()
                  if 'Entity' in labs[i] and 'Event' not in labs[i] and i in adjacency]
    seeds = [i for _,i in sorted(candidates)[:100]]
    reach = []
    for seed in seeds:
        visited, front, counts = {seed}, {seed}, []
        for depth in range(3):
            nxt = {b for a in front for b in adjacency.get(a,())} - visited
            visited.update(nxt); front = nxt; counts.append(len(visited)-1)
        reach.append(counts)
    reach_summary = {str(d+1): {'mean_cumulative_reachable_nodes': round(statistics.mean(r[d] for r in reach),3),
                              'median_cumulative_reachable_nodes': statistics.median(r[d] for r in reach),
                              'max_cumulative_reachable_nodes': max(r[d] for r in reach)}
                     for d in range(3)} if reach else {}
    out = {'release_version': manifest['version'], 'audit_date_utc': datetime.now(timezone.utc).isoformat(),
           'files': checks, 'nodes': n, 'edges': sum(relations.values()), 'duplicate_node_ids': duplicate_nodes,
           'node_kinds': dict(kinds), 'node_labels_nonexclusive': dict(labels), 'nodes_with_name': name_count,
           'node_field_counts': dict(node_fields), 'edge_field_counts': dict(edge_fields),
           'unexpected_node_fields': dict(unexpected_n), 'unexpected_edge_fields': dict(unexpected_e),
           'edge_types': dict(types), 'relation_counts': dict(relations), 'relations_with_sources': dict(sourced),
           'source_count_distribution': dict(source_sizes), 'self_loops_by_relation': dict(selfloops),
           'claim_projection_findings': dict(claim_issues), 'integrity_findings': dict(issues),
           'date_field_nonempty_counts': dict(date_present), 'date_parse_findings': dict(date_bad),
           'date_value_types': dict(date_types),
           'date_ranges_lexical_iso': {k: {'min': min(v),'max':max(v)} for k,v in dates.items()},
           'relations_with_any_time_field': dict(rel_dated),
           'full_graph': full.summary(range(n)), 'semantic_projection': semantic.summary(active_s),
           'claim_projection': claims.summary(active_c),
           'reachability': {'projection': 'all RELATES_TO directed edges, no semantic claim of causation',
                            'eligible_seeds': len(candidates), 'sample_size': len(seeds),
                            'selection': 'first 100 Entity-labelled non-Event nodes with outgoing semantic edges, ordered by SHA256(node id)',
                            'hops': reach_summary},
           'elapsed_seconds': round(time.monotonic()-start,3)}
    out['manifest_counts_match'] = n == manifest['node_count'] and out['edges'] == manifest['edge_count']
    out['manifest_relation_counts_match'] = dict(relations) == manifest['relation_counts']
    out['manifest_source_counts_match'] = {k:v for k,v in sourced.items() if v} == manifest['relations_with_source_episodes']
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'output':str(args.output),'nodes':n,'edges':out['edges'],'elapsed_seconds':out['elapsed_seconds']}))


if __name__ == '__main__':
    main()
