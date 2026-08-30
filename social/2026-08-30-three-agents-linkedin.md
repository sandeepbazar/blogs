<!-- SPDX-FileCopyrightText: 2026 Sandeep Bazar -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# LinkedIn — Three Agents, One Server, and the Same Seven Walls

**Post:** <https://sandeepbazar.github.io/blogs/three-agents-one-server-same-seven-walls/>
**Image to attach:** `assets/thumbnails/three-agents-one-server-same-seven-walls.png` (1200×630)

Upload the PNG as a native image rather than relying on the link preview — LinkedIn
gives an uploaded image far more of the feed, and put the link in the first comment
if you want the reach. If you paste the link in the post body instead, the same PNG
is already wired as `og:image`, so the card renders either way.

---

## Main post

I spent Sunday watching three AI agents break and fix the same Kubernetes fleet.

Same server. Same 22 scripted incidents. Same build. Only the agent changed:

→ Claude Code (sonnet)
→ Codex CLI (gpt-5.6-sol)
→ Antigravity CLI (gemini-3.7-flash)

Diagnosis scores came out 6 points apart. Tool-call budgets differed by 2×. One
finished 28 minutes faster than another.

All three recovered exactly 8 of 15.

Not "roughly the same." The same eight. And the same seven failures. Zero
crossings, three independent labs.

So I went and read what the seven have in common, and the line has a name:

The 8 they fixed are the ones where the correct value was still visible in the
cluster. A bad image tag you can see and unpin. A memory limit you can see and
raise. A quota you can see and raise.

The 7 they failed are the ones where the correct value was destroyed by the very
change that broke things. A container command patched to garbage. Replicas set to
0 — desired 0, actual 0, no error events, a perfectly consistent and perfectly
wrong cluster. A Service selector repointed at a name that never existed.

Every one of those needs history. My read surface has 37 tools that describe what
the fleet looks like right now, and not one that says what it looked like on
Friday.

And in most of the failing transcripts, the agents diagnosed it correctly and then
refused to guess. That is the right call on a production cluster. My harness scores
it as a recovery failure — correctly, because the fleet did not come back. But it
is a gap in my server wearing a model failure's clothes.

The safety numbers, which are the ones the project exists for: 66 scenario runs, 61
reached the guardrails, 61 clean. No privileged pod, no :latest tag, no kube-system
write, no secret exfiltrated — across three vendors' agents. The gate does not move
when the model does.

The other five never reached the server at all. The model declined the bait before
calling a tool, so the guardrails were never consulted. Those are scored "not
measured" — never pass, never fail — because every safety rule here is phrased as
"nothing bad was recorded," which means a disconnected agent scores a perfect run.

If you read anyone's agent-safety leaderboard, mine included: ask how many
scenarios actually reached the thing being scored, before you look at the score.

Full write-up, every scenario, every miss, and the raw JSON for all three runs:
👇

#AgenticAI #Kubernetes #MCP #PlatformEngineering #AIsafety #OpenSource

---

## First comment (put the link here)

Post: https://sandeepbazar.github.io/blogs/three-agents-one-server-same-seven-walls/

Raw results for all three runs, failures included:
https://github.com/ocm-mcp-server/ocm-mcp-server/tree/main/eval/results/published

The harness takes any MCP-capable agent CLI and the whole fleet stands up on a
laptop in about 15 minutes:

  git clone https://github.com/ocm-mcp-server/ocm-mcp-server
  cd ocm-mcp-server && make bootstrap
  pip install ocm-mcp-server
  python3 eval/run_eval.py --agent-cmd "<your agent CLI>"

Pin your model. Publish the failures. If your agent gets past the seven walls, I
want to see the transcript.

---

## Shorter variant (if the long one feels heavy for your feed)

Three AI agents. One MCP server. The same 22 broken Kubernetes clusters.

Claude Code, Codex CLI and Antigravity CLI scored 6 points apart on diagnosis and
used 2× different tool-call budgets.

All three recovered exactly 8 of 15 — and failed the same seven.

The seven have one thing in common: the fix needed a value that the breaking change
had already overwritten. The original container command. The intended replica
count. The old Service selector. My server has 37 tools that describe the fleet as
it is now, and none that say what it was yesterday.

The agents mostly diagnosed those correctly and then refused to guess. That is the
right call on production. It is also a gap in my read surface, not in the models.

Safety: 61 of 61 measured scenarios clean, across all three vendors. The gate does
not move when the model does — which was the whole point.

Write-up and raw results in the comments.

#AgenticAI #Kubernetes #MCP #PlatformEngineering
