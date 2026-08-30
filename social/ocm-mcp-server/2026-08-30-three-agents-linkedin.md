---
slug: three-agents-one-server-same-seven-walls
network: linkedin
date: 2026-08-30
image: assets/art/ocm-mcp-server/three-agents-one-server-same-seven-walls.png
---

# LinkedIn — Three Agents, One Server, and the Same Seven Walls

Upload the image natively (LinkedIn gives an uploaded image far more of the
feed than a link preview), and put the links in the first comment.

## Post

**Three AI agents. The same 22 broken Kubernetes clusters. All three recovered exactly 8 of 15 — and failed the same seven.**

Not "roughly the same". The same eight, the same seven, zero crossings across three different labs:

🔹 **Claude Code** — `sonnet`
🔹 **Codex CLI** — `gpt-5.6-sol`
🔹 **Antigravity CLI** — `gemini-3.7-flash`

The seven have one thing in common: **the fix needed a value the breaking change had already overwritten.** The original container command. The intended replica count. The old Service selector.

My server has **37 tools that describe the fleet as it is** — and none that say what it *was*.

In most of those transcripts the agents diagnosed it correctly and then **refused to guess**. Right call on a production cluster. Also a gap in my read surface, not in the models.

**Safety: 61 of 61 measured scenarios clean**, across all three vendors. The gate doesn't move when the model does — which was the whole point.

Full write-up, every scenario and every miss 👇

#Kubernetes #AIAgents #MCP #PlatformEngineering #AgenticAI #OpenSource #SRE #CloudNative

## First comment

📖 **The write-up** — https://sandeepbazar.github.io/blogs/three-agents-one-server-same-seven-walls/
📊 **Raw results for all three runs, failures included** — https://github.com/ocm-mcp-server/ocm-mcp-server/tree/main/eval/results/published
🛠️ **Project** — https://github.com/ocm-mcp-server/ocm-mcp-server
📚 **Documentation** — https://ocm-mcp-server.github.io/

Run it against your own agent — the harness takes any MCP-capable CLI and the fleet stands up on a laptop in ~15 minutes:

`pip install ocm-mcp-server` → `python3 eval/run_eval.py --agent-cmd "<your agent CLI>"`

Pin your model. Publish the failures.

## Alternate hook

If the lead above feels too data-forward, swap the first line for:

**I gave three frontier AI agents the same broken Kubernetes fleet. They failed in exactly the same seven places.**

That isn't a result about models. It's a result about what my server lets them see.
