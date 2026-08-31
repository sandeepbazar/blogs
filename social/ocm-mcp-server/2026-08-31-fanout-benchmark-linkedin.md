---
slug: why-fan-out-measures-1-2x-on-localhost
network: linkedin
date: 2026-08-31
image: assets/art/ocm-mcp-server/why-fan-out-measures-1-2x-on-localhost.png
---

# LinkedIn: Why concurrent fan-out benchmarks at 1.2x on localhost

Blog link in the post body so LinkedIn renders the card from the page's
`og:image`. Do not also upload an image, it replaces the preview.

## Post

Eight worker threads. Twenty Kubernetes clusters to scan. Measured speedup: **1.2x.**

Not 8x. The reason is worth knowing before you benchmark any fan-out.

Scanning spokes one at a time costs the **sum** of their latencies. Scanning them concurrently costs closer to the **largest single** latency.

Every apiserver in that benchmark runs as a local process on one machine. Latency between them is near zero. When every latency is near zero, the sum and the largest converge, and there is nothing left for concurrency to win. What 1.2x measures is thread-pool overhead against local process scheduling.

Distribute those spokes across regions, where each call pays tens to hundreds of milliseconds, and the two quantities separate. With as many spokes as workers at comparable latency, the expected speedup approaches the worker count.

**So 1.2x is a floor, not a ceiling**, produced under the friendliest possible conditions for the sequential path it competes against.

Three ways to report that, one of which survives a re-run:

→ "Up to 8x faster" is a projection presented as a measurement.
→ Dropping the fan-out removes what matters on a real fleet because a localhost test cannot see it.
→ "1.2x, and here is why it is a floor" is reproducible and says which direction the error points.

If you benchmark a read path that both paginates and fans out, measure the two separately. They have independent scaling limits, and one combined number hides which one your fleet hits first.

Method, both phases, and every caveat:
https://sandeepbazar.github.io/blogs/ocm-mcp-server/why-fan-out-measures-1-2x-on-localhost/

#Kubernetes #Benchmarking #Performance #PlatformEngineering #MCP #OpenSource #SRE #CloudNative

## First comment

📊 **Method, versions and caveats**: https://github.com/ocm-mcp-server/ocm-mcp-server/blob/main/docs/benchmarks.md
🛠️ **Project**: https://github.com/ocm-mcp-server/ocm-mcp-server
📚 **Documentation**: https://ocm-mcp-server.github.io/

The other phase: 1,023 ManagedCluster objects read from the hub in 0.083s, because the list follows the apiserver's own continue tokens instead of requesting the whole collection. At the 5,000-item ceiling the response carries an explicit truncation marker, since an agent handed 5,000 of 7,000 clusters with no warning reports confidently on a fleet missing 2,000 machines.

Those 1,000 are custom resources, not clusters. No apiserver behind them. It measures hub-side storage and pagination and nothing else.

Run it:

`bash hack/bootstrap.sh` → `python3 hack/bench_fleet.py --phase fanout`

Spokes in more than one region measure the regime a single machine cannot.

## Alternate opening

A benchmark that makes your own feature look unnecessary is the most credible number you can publish.

Concurrent fan-out across 20 Kubernetes clusters: 1.2x. Here is why that number is a floor rather than a verdict.
