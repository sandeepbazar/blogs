---
title: "My Concurrency Benchmark Came Back at 1.2x. I Published It Anyway."
dek: "I built concurrent fan-out across a Kubernetes fleet, measured it honestly, and got a speedup barely worth the code. The number is real. It is also a lower bound, and explaining why turned out to be more useful than a better number would have been."
date: 2026-08-31
slug: the-benchmark-that-undersold-my-own-code
category: "Kubernetes & MCP"
cover: assets/art/ocm-mcp-server/the-benchmark-that-undersold-my-own-code.svg
card: assets/art/ocm-mcp-server/the-benchmark-that-undersold-my-own-code.png
tags: [benchmarking, kubernetes, mcp, performance, kwok]
canonical: self
status: published
---
![Two benchmark phases: 1,023 clusters read in 0.083 seconds on the hub, and a 1.2x fan-out speedup across 20 kwok apiservers that is a lower bound, not a ceiling](/blogs/assets/art/ocm-mcp-server/the-benchmark-that-undersold-my-own-code.svg)

I added a thread pool so that asking "is my fleet healthy?" would scan every
cluster at once instead of one after another. Then I benchmarked it.

**1.2x.**

Not 8x, which is what eight workers ought to buy you. Barely enough to justify
the import. I had a `concurrent.futures.ThreadPoolExecutor`, a config knob, and a
number that made both look like a waste of time.

My first instinct was to not publish it. My second was to delete the thread pool.
What I did instead was work out why the number was so small, which turned out to
be the useful part.

## What was being measured

[`ocm-mcp-server`](https://github.com/ocm-mcp-server/ocm-mcp-server) gives an AI
agent read access to a multi-cluster Kubernetes fleet through an
[Open Cluster Management](https://open-cluster-management.io/) hub. The tool
under test is `fleet_health`, which answers the whole-fleet question in one call
and does it in two phases:

1. **One paged list on the hub** for every cluster's conditions.
2. **A concurrent scan of each spoke** for unhealthy pods and degraded
   deployments, on a bounded worker pool.

Those two phases fail at different scales. The first one struggles when the hub
holds thousands of `ManagedCluster` objects; the second struggles when the spokes
are far away. A single `fleet_health` number would have averaged the two into
something that describes neither, so they get separate benchmarks and separate
fixtures.

## Phase one: 1,000 clusters on the hub

The hub-side question is whether a list stays fast as a fleet grows. So the
benchmark applies **1,000 fake `ManagedCluster` CRs** to a real kind hub and
reads them back.

| scenario | best | median |
|---|---|---|
| `list_clusters` @ 1,023 clusters | 0.079 s | 0.083 s |
| `fleet_health` (hub only) @ 1,000 clusters | 0.083 s | 0.087 s |

A fleet two orders of magnitude larger than my test fleet reads back in under a
tenth of a second. That works because the list follows the apiserver's own
`continue` tokens instead of asking for everything at once:

```python
res = list_fn(*args, limit=LIST_PAGE_SIZE, **kwargs)
items.extend(res.get("items", []) or [])
cont = (res.get("metadata") or {}).get("continue") or ""
```

Pages of 500, up to a 5,000-item ceiling, and when it hits that ceiling it says
so in the response rather than returning a short list that looks complete. That marker matters more than the speed does: an agent handed 5,000 of 7,000
clusters with no warning will give you a confident report about a fleet with
2,000 machines missing from it.

One caveat belongs right here rather than in a footnote. **Those are 1,000 custom
resources, not 1,000 clusters.** There is no apiserver behind them and no
klusterlet, so this measures hub-side API storage and pagination and nothing else.
"A 1,000-cluster benchmark" would be the more impressive phrase, which is exactly
why the doc says the boring version twice.

## Phase two: 20 real apiservers, and the disappointing number

Fan-out needs real apiservers to answer real list calls, and 1,000 apiservers do
not fit on a laptop. So the second phase uses [kwok](https://kwok.sigs.k8s.io/)
to stand up **20 independent kube-apiservers**, each with a fake node and about
50 pods that kwok's controller drives straight to `Running`. Every spoke is
registered on the hub and wired into the server's spoke contexts, so the scan
does a genuine pod and deployment list against a genuine apiserver.

| scenario | best | median |
|---|---|---|
| sequential (`workers=1`) @ 20 spokes | 0.356 s | 0.367 s |
| concurrent (`workers=8`) @ 20 spokes | 0.299 s | 0.302 s |

Eight workers, twenty spokes, and 65 milliseconds. That is the 1.2x.

## Why the number is small, and why that is the finding

All twenty kwok apiservers are local processes on one machine, so per-spoke
round-trip latency is close to zero. That one fact explains the whole result.

Scanning spokes one at a time costs the sum of their latencies. Scanning them
concurrently costs closer to the largest single latency. When every latency is
near zero, the sum and the largest are almost the same number, so there is
nothing for concurrency to win. What the 1.2x actually measures is thread
overhead against local process scheduling.

Put those same spokes in three regions instead of one laptop, where each call
pays tens to hundreds of milliseconds, and the arithmetic inverts: with at least
as many spokes as workers at comparable latency, the expected speedup approaches
the worker count. Eight, at the default, not 1.2.

So 1.2x is **a lower bound, measured under the friendliest possible conditions
for the code it was competing against.** The benchmark cannot reach the situation
the feature exists for, and a laptop cannot host that situation.

That leaves the question of what to write down. "Up to 8x faster" is a projection
wearing a measurement's clothes. Deleting the thread pool would throw away the
thing that matters on a real fleet because a localhost test could not see it.
Publishing 1.2x with the reason attached is the only version that survives
someone re-running it.

## What I would do differently

**Benchmark the failure modes separately.** One `fleet_health` number would have
averaged a pagination test and a latency test into something that describes
neither. They break at different scales and deserve different fixtures.

**Name the simulation in the same breath as the result.** Not in a footnote. The
words "1,000 clusters" and "CRs only, no apiserver" belong in the same sentence,
because the gap between them is exactly where a reader's imagination fills in
something better than what you measured.

**Say which direction your error points.** "This is a lower bound" is far more
useful than a confidence interval nobody computed. A reader who knows the number
can only go up with real latency can reason about their own fleet. A bare 1.2x
tells them to skip the feature.

**Publish the disappointing one.** The 1.2x is the most credible number in the
repository precisely because it makes my own code look unnecessary. Nobody has to
wonder whether I tuned the benchmark until it agreed with me.

## Run it yourself

```bash
git clone https://github.com/ocm-mcp-server/ocm-mcp-server
cd ocm-mcp-server
bash hack/bootstrap.sh                              # kind hub + 3 spokes

OCM_MCP_HUB_CONTEXT=kind-hub python3 hack/bench_fleet.py --phase hub
OCM_MCP_HUB_CONTEXT=kind-hub python3 hack/bench_fleet.py --phase fanout
```

Each figure is the min and median of five repetitions. The script removes its
1,000 fake CRs and its kwok clusters afterwards and leaves your fleet alone.

If you have spokes in more than one region, that run measures something my laptop
cannot, and I would genuinely like to see the number. The method and every caveat
are in
[`docs/benchmarks.md`](https://github.com/ocm-mcp-server/ocm-mcp-server/blob/main/docs/benchmarks.md).

---

*`ocm-mcp-server` is Apache-2.0. [GitHub](https://github.com/ocm-mcp-server/ocm-mcp-server) ·
[docs](https://ocm-mcp-server.github.io/) · [PyPI](https://pypi.org/project/ocm-mcp-server/).
Related: [the three-agent evaluation](/blogs/three-agents-one-server-same-seven-walls/),
where publishing the failures was also the point.*
