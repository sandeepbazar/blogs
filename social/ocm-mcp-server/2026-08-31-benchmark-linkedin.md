---
slug: the-benchmark-that-undersold-my-own-code
network: linkedin
date: 2026-08-31
image: assets/art/ocm-mcp-server/the-benchmark-that-undersold-my-own-code.png
---

# LinkedIn: My Concurrency Benchmark Came Back at 1.2x

Blog link goes in the post body so LinkedIn renders the card from the page's
`og:image`. Do not also upload an image, it replaces the preview.

## Post

I built concurrent fan-out so an AI agent could check every cluster in a fleet at once instead of one after another.

Then I benchmarked it. **1.2x.**

Eight workers, twenty spokes, and a 65-millisecond improvement. My first instinct was to not publish it.

Here is why the number is small, and why that is the actual finding:

All twenty apiservers in the benchmark run as local processes on one machine. Latency between them is close to zero.

Scanning spokes one at a time costs the **sum** of their latencies. Scanning them concurrently costs closer to the **largest single** latency. When every latency is near zero, the sum and the largest are almost the same number. There is nothing for concurrency to win.

Put those spokes in three regions and the arithmetic inverts. With as many spokes as workers at real network latency, the speedup approaches the worker count. Eight, not 1.2.

So 1.2x is a **lower bound measured under the friendliest possible conditions for the code it was competing against**, and my laptop cannot host the case the feature exists for.

"Up to 8x faster" would be a projection wearing a measurement's clothes. Deleting the thread pool would throw away the thing that matters on a real fleet because a localhost test could not see it.

Publishing 1.2x with the reason attached is the only version that survives someone re-running it. It is the most credible number in the repo precisely because it makes my own code look unnecessary.

Full write-up, both benchmark phases, and every caveat:
https://sandeepbazar.github.io/blogs/the-benchmark-that-undersold-my-own-code/

#Kubernetes #Benchmarking #Performance #PlatformEngineering #MCP #OpenSource #SRE #CloudNative

## First comment

📊 **Method, results and caveats**: https://github.com/ocm-mcp-server/ocm-mcp-server/blob/main/docs/benchmarks.md
🛠️ **Project**: https://github.com/ocm-mcp-server/ocm-mcp-server
📚 **Documentation**: https://ocm-mcp-server.github.io/

The other half of the benchmark: 1,000 fake ManagedCluster CRs on the hub read back in 0.083s, because the list follows the apiserver's own continue tokens instead of asking for everything at once.

Those are 1,000 custom resources, not 1,000 clusters. No apiserver behind them. Saying so costs the headline and keeps the number honest.

Run it on your own fleet:

`bash hack/bootstrap.sh` → `python3 hack/bench_fleet.py --phase fanout`

If your spokes are in more than one region, that run measures something mine cannot.

## Alternate opening

Three ways to handle a benchmark that makes your feature look pointless:

1. Do not publish it.
2. Delete the feature.
3. Work out why the number is small.

Only the third one is interesting.
