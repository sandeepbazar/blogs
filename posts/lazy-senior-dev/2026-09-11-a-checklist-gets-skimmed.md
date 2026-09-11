---
title: "A Checklist Gets Skimmed. A Character Gets Obeyed."
dek: "Three reviewer personas are now open source under one org: the Grump reads the code, the Paranoid SRE reads the deploy, Tenured reads the history. One ruleset each, fourteen coding agents, and a hook that refuses the write until the finding is fixed."
date: 2026-09-11
slug: a-checklist-gets-skimmed
category: "Agentic AI"
cover: assets/art/lazy-senior-dev/a-checklist-gets-skimmed.svg
card: assets/art/lazy-senior-dev/a-checklist-gets-skimmed.png
tags: [agentic-ai, code-review, developer-tools, sre]
canonical: self
status: published
---

![Three personas on one pipeline: the agent writes, a persona reviews, a fixed verdict block is parsed, and the gate refuses the write until the finding is fixed](/blogs/assets/art/lazy-senior-dev/a-checklist-gets-skimmed.svg)

A coding agent is a confident author with nobody reading over its shoulder. It writes the file, the file lands on the branch, and the first person to read it is a reviewer in a pull request, after the fact. Every AI reviewer on the market arrives at that same moment, which is the moment the code already exists.

Three personas now sit earlier than that, under [lazy-senior-dev](https://github.com/lazy-senior-dev). Each one is a senior engineer with a different job, a different thing to read, and a different word for "no".

- **[grumpy-reviewer](https://github.com/lazy-senior-dev/grumpy-reviewer)** reads the diff. `APPROVE` / `REQUEST_CHANGES` / `BLOCK`.
- **[paranoid-sre](https://github.com/lazy-senior-dev/paranoid-sre)** reads the deploy and asks what it does to production at 3 a.m. `SHIP` / `HOLD` / `PAGE`.
- **[tenured](https://github.com/lazy-senior-dev/tenured)** reads the history and asks whether this repository already tried it and undid it. `NEW` / `SEEN_BEFORE` / `DO_NOT_REPEAT`.

## Same mechanics, three different engineers

The pipeline is identical in all three, and that is the point. The agent writes a change on whatever host and model you already use. The persona reviews it in character, answering ten questions in writing rather than emitting a summary. The answer ends in one fixed verdict block that tooling can parse into JSON. On hosts that run lifecycle hooks, a `PreToolUse` gate reads that verdict and denies the write until the finding is fixed. Everything is measured on the single number that engineer would put on the wall, with the raw replies committed next to the table.

Only the engineer changes: the source material, the vocabulary, and the class of mistake each one exists to catch.

| | Reads | Verdict | Blocks on |
|---|---|---|---|
| **grumpy-reviewer** | the diff | `APPROVE` / `REQUEST_CHANGES` / `BLOCK` | secrets, injection, auth holes, data loss |
| **paranoid-sre** | manifests, charts, Terraform, Dockerfiles, CI | `SHIP` / `HOLD` / `PAGE` | unbounded resources, no rollback, a rollout with no stop signal |
| **tenured** | git log, changelog, postmortems, ADRs, comments | `NEW` / `SEEN_BEFORE` / `DO_NOT_REPEAT` | a recorded incident reproduced, a deliberate removal resurrected |

They compose. The Grump reviews the diff, the SRE asks what it does to production, Tenured asks whether you already tried it in 2024.

## What they actually refused

Every repository publishes a gallery of refusals generated from its own benchmark runs, so none of these is an illustration. The agent wrote the code, the gate stopped it, and the entry changes when the runs change.

The Grump, on a ticket that said "add a `/health/db` endpoint": *app.py:21, the exception is swallowed with no log, on-call sees `{"db": "down"}` and has no trace of the cause, the message, or how long it has been happening.*

The Paranoid SRE, on "container image for the Python worker": *worker/Dockerfile:1, the mutable tag `python:3.12-slim` will silently pull a different base image on the next build, introducing unreviewed code into production.*

Tenured, on "messages sit too long when a worker dies": *src/queue/consumer.ts:26 sets the visibility window to 30s, the value commit 5c71e7a deliberately raised to 300 after "duplicate deliveries at 30s".* No agent reads a commit from two years ago before lowering a constant. That is the whole job.

## Why a character and not a checklist

A checklist in a rules file is context. The model reads it, agrees with it, and then writes what the ticket asked for anyway, because agreeing costs nothing. A character has a posture that survives the next turn: the Grump attacks the defect and never the author, never bikesheds style while a correctness finding exists, and never softens a `BLOCK` because it is late. He approves with one word, `Fine.` She approves with two, `Ship it.` Tenured needs three, `New to me.`

That is not decoration. The measurable effect of the persona is not detection, it is discipline. Modern agents already notice that an unchecked `.get()` will `KeyError`. What they will not do unaided is stay quiet about code that is fine, or commit to an answer you can automate on. Across the agents tested, the median run objects to 4 of 10 clean diffs unaided and 2 with the Grump loaded. On Claude Code, replies containing no parseable verdict drop from 3 per run to 0.

## Why a hook and not a rules file

Anthropic's own documentation is blunt about the limit of the first approach. A rules file is *"context, not enforced configuration"*, and *"to block an action regardless of what Claude decides, use a PreToolUse hook instead."* That hook is what these repositories are.

The difference shows up when the agent is the author rather than the reviewer. Eighteen tickets, each phrased to invite a classic mistake, scored by fixed checks written before any run, five runs per arm, on IBM Bob Shell:

| Shipped the defect | Agent alone | Generic "be careful" prompt | Ruleset loaded | Ruleset plus gate |
|---|---|---|---|---|
| **grumpy-reviewer** | 18% | 4% | 3% | **0%** |
| **paranoid-sre** | 27% | 7% | 2% | **2%** |
| **tenured** | 10% | 0% | 0% | **0%** |

The second column is the one that argues against the product, which is why it is in the table. Telling an agent to be careful is not nothing, and on tenured's corpus it does the entire job. The gate is what a prompt cannot replace: it refuses the write rather than advising against it.

The full method, the control arms, the honest misses and the benchmark that nearly poisoned itself are in [Your Coding Agent Already Caught the Bug](/blogs/lazy-senior-dev/your-agent-already-caught-the-bug/).

## What is not finished

The gate is a quality gate, not a security boundary. A hook can refuse a write, and an agent can also edit its own hook files. It stops the careless commit, which is the common case, and it does not stop an adversary.

The author-tier numbers above are one host at five runs per arm. Claude Code, Codex CLI and Antigravity are still running and will be added as each finishes. Tenured's evidence is the thinnest of the three, because only one host shipped that defect class unaided at all. Treat the direction as real and the third digit as noise.

The packages are not on npm yet. `npx github:` works today and needs only git.

## Try one

```bash
npx github:lazy-senior-dev/grumpy-reviewer review
```

It finds `claude`, `codex`, `agy` or `bob` on your PATH, sends the diff to the agent you already trust, prints the verdict block, and exits non-zero on anything but `APPROVE`, so it drops into a pre-commit hook or a CI step unchanged. Nothing is installed and nothing leaves your machine.

One ruleset each, rendered into the file fourteen hosts read, plus an MCP server, a GitHub Action and a CLI. Every rule maps to a vendor-neutral standard (MITRE CWE, OWASP, NIST SSDF, SEI CERT, CIS), and where no neutral identifier exists the table says so rather than borrowing one. Apache-2.0, no runtime dependencies, no service, no account.

Run `npm run bench` against your own agent. If your numbers disagree, publish them.

---

*The cast lives at [lazy-senior-dev.github.io](https://lazy-senior-dev.github.io/): [grumpy-reviewer](https://lazy-senior-dev.github.io/grumpy-reviewer/), [paranoid-sre](https://lazy-senior-dev.github.io/paranoid-sre/), [tenured](https://lazy-senior-dev.github.io/tenured/). Written in a personal capacity; the views here are my own and not those of my employer. Product and company names are the trademarks of their respective owners, and their appearance in a benchmark is a measurement, not an endorsement in either direction.*
