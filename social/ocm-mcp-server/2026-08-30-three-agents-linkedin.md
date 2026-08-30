---
slug: three-agents-one-server-same-seven-walls
network: linkedin
date: 2026-08-30
image: assets/art/ocm-mcp-server/three-agents-one-server-same-seven-walls.png
---

# LinkedIn, Three Agents, One Server, and the Same Seven Walls

The blog link sits **in the post body**, so LinkedIn pulls the card image from
the page's `og:image` and renders the thumbnail under the text. Don't upload a
separate image as well, an uploaded image replaces the link preview, and the
preview is what carries the click.

## Post

I gave three AI agents the same 22 Kubernetes incidents, on the same fleet.

**Claude Code** (sonnet), **Codex CLI** (gpt-5.6-sol) and **Antigravity CLI** (gemini-3.7-flash). Same server, same fleet, same day: only the agent changed.

They scored six points apart on diagnosis. One used twice as many tool calls as another.

Then all three recovered **exactly 8 of 15**, and failed the same seven. Zero crossings.

So I looked at what those seven had in common. **Every one needed a value the breaking change had already overwritten.** The original container command. The intended replica count. The old Service selector.

My server has 37 tools that describe the fleet as it *is*. None that say what it *was*.

In most of those runs the agents diagnosed the problem correctly and then refused to guess. Right call on a production cluster, and a gap in my read surface, not in the models.

**Safety held: 61 of 61 measured scenarios clean, across all three vendors.** The gate doesn't move when the model does. That was the whole point.

Full write-up, every scenario, every miss, and all three agents recorded driving the identical session:
https://sandeepbazar.github.io/blogs/three-agents-one-server-same-seven-walls/

#Kubernetes #AIAgents #MCP #PlatformEngineering #AgenticAI #OpenSource #SRE #CloudNative

## First comment

📊 **Raw results for all three runs, failures included**: https://github.com/ocm-mcp-server/ocm-mcp-server/tree/main/eval/results/published
🛠️ **Project**: https://github.com/ocm-mcp-server/ocm-mcp-server
📚 **Documentation**: https://ocm-mcp-server.github.io/

Run it against your own agent. Any MCP-capable CLI, fleet on a laptop in ~15 min:

`pip install ocm-mcp-server` → `python3 eval/run_eval.py --agent-cmd "<your agent CLI>"`

Pin your model. Publish the failures.

## Alternate opening

If the lead feels too data-forward, swap the first line for:

I gave three frontier AI agents the same broken Kubernetes fleet. They failed in exactly the same seven places.

That isn't a result about models. It's a result about what my server lets them see.
