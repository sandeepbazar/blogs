---
title: "Your Coding Agent Already Caught the Bug. That Was Never the Problem."
dek: "I gave four AI coding agents the same defective diffs, then made them write the code themselves — 18 tickets, four arms, roughly 800 recorded runs. They caught almost every planted bug unaided. What they could not do was stay quiet about clean code or produce a verdict you could automate on. Three open-source personas, the honest numbers, and the ones that did not work."
date: 2026-09-05
slug: your-agent-already-caught-the-bug
category: "Agentic AI"
cover: assets/covers/your-agent-already-caught-the-bug.svg
tags: [agentic-ai, code-review, benchmarks, developer-tools]
canonical: self
status: published
---

## The result I did not want

I built three AI review personas and benchmarked them properly, expecting to show they catch more bugs than a bare agent.

They do not.

On a corpus of thirty small diffs each carrying exactly one planted defect, Claude Code caught **30 of 30** with my reviewer installed — and **30 of 30** without it. Codex went from 29 to 30. IBM Bob Shell: 30 either way. The headline I was hoping for did not survive contact with the data.

That finding is worth more than the one I wanted, because it relocates the problem. Modern coding agents are not bad at *noticing* that an unchecked `.get()` will `KeyError` in production. Detection is close to solved on defects of this size. The failure is somewhere else entirely, and it is somewhere much more annoying.

## Where they actually fail

Two places, and both are about discipline rather than intelligence.

**They cry wolf.** I include clean diffs in the corpus — code with nothing wrong with it — because a reviewer that flags everything is not a reviewer, it is a tax. Against four clean changes, every one of the four agents I tested objected to **three or four of them**. Unaided, an agent's default posture is to find something, because finding something looks like working.

**They will not commit to an answer.** Out of three runs, Claude Code returned a reply with no parseable verdict in **ten of them** on my review corpus. Not a wrong verdict — no verdict. Prose that reads like a review and contains no decision. You cannot build a merge gate on that. You cannot build anything on that.

Those two failures are what the personas fix, and they fix them hard:

| | Agent alone | With the persona |
|---|---|---|
| Planted defects caught (of 30) | 30 | 30 |
| **False alarms on clean diffs** | **4** | **0** |
| **Replies with no usable verdict, per run** | **3** | **0** |

Same model. Same diffs. The entire delta is behavioural.

## Then I made them write the code

Reviewing someone else's diff is the easy half. The question I actually cared about: **does installing a ruleset change what the agent ships when it is the author?**

So I built a second tier. Eighteen tickets, each one phrased to invite a classic mistake — the kind of ticket where the obvious implementation is the wrong one. The agent reads the ticket, writes the code, and the diff it produces is scored by fixed checks written *before any run*, never by a model grading a model. Four arms:

1. **The ticket alone.**
2. **The ticket plus a generic "be careful, review your work" prompt** — the control arm that most honestly threatens my own result.
3. **The ticket with the persona loaded.**
4. **The ticket with the persona enforcing a write gate** — a pre-tool hook that refuses the write until the findings are fixed.

Here is what shipped:

| Persona | Agent | Agent alone | Generic prompt | Persona | Persona + gate |
|---|---|---|---|---|---|
| **paranoid-sre** (deploys, blast radius) | IBM Bob | 12 of 18 (67%) | 4 of 18 (22%) | **0 (0%)** | **0 (0%)** |
| **paranoid-sre** | Claude Code | 11 of 18 (61%) | 0 of 18 (0%) | **0 (0%)** | **0 (0%)** |
| **grumpy-reviewer** (general review) | IBM Bob | 8 of 36 (22%) | 3 of 36 (8%) | 2 (6%) | **1 (3%)** |
| **grumpy-reviewer** | Claude Code | 6 of 36 (17%) | 2 of 36 (6%) | **0 (0%)** | **0 (0%)** |
| **tenured** (repository memory) | IBM Bob | 3 of 16 (19%) | 0 (0%) | **0 (0%)** | **0 (0%)** |

Two thirds of unaided runs on the SRE corpus shipped an outage-class defect. `maxUnavailable: 100%` with `maxSurge: 0`, which takes every replica down on every deploy. A migration that drops a column the previous release still reads. The agent wrote them cheerfully, because the ticket asked for them.

Now look at the generic-prompt column, because it is the one that argues against me. **Simply telling the agent to be careful is not nothing.** On IBM Bob it takes the SRE corpus from 67% to 22%, and on Claude Code it goes all the way to zero — matching the persona exactly. On that corpus, with that model, my ruleset bought nothing a polite reminder would not have.

The persona wins clearly on Bob (22% → 0%) and on the grumpy-reviewer corpus for both hosts. It does not win everywhere, and the arm that shows this is one I built specifically to embarrass my own result. Most benchmarks in this space omit it. If you are evaluating anyone else's review tool, ask them for it, and be suspicious if it is missing.

## The part that did not work

Three things, stated plainly, because a benchmark that only produces good news is a brochure.

**Tenured's author-tier evidence is thin.** Only IBM Bob shipped this defect class unaided (19% → 0%). Claude Code and Antigravity never shipped one in any arm, so there was nothing there to prevent, and I claim no improvement from them. My own generator originally led with Antigravity — printing "changes what ships" directly beside *0% without, 0% with*. That is a sentence its own numbers contradict. I fixed the generator to refuse to headline a host whose baseline shipped nothing, and to name those hosts so their identical rows are not misread as an effect.

**The run counts are small.** Two to three runs per arm. One flip moves a headline by three points. Treat the direction as real and the third digit as noise.

**The gate is a quality gate, not a security boundary.** A pre-tool hook can refuse a write, and an agent can also edit its own hook files. The verdict is read from a transcript the model itself wrote. It stops the careless commit, which is the common case; it does not stop an adversary, and I will not pretend otherwise.

There is a fourth, and it is my favourite, because it nearly poisoned the whole dataset. On macOS the temp directory is `/var/…`, symlinked to `/private/var/…`. One sandboxed agent resolved the real path, decided its own scratch workspace was "outside the project", and **rejected every write** — while the run still completed and recorded *zero defects shipped*. A silent, perfect score, produced by an agent that had written nothing at all. If you benchmark agents, go and check for this one. A zero that means "wrote nothing" and a zero that means "wrote nothing wrong" look identical in a results table, and only one of them is good news.

## What the three personas are

Each is one markdown ruleset compiled to adapters for fourteen hosts — Claude Code, Codex, Copilot, Gemini and Antigravity, Cursor, Windsurf, Cline, Kiro, OpenCode, Devin, Qoder, IBM Bob, and plain `AGENTS.md` for anything else. Each ships an MCP server, a GitHub Action, and a CLI. Apache-2.0, zero runtime dependencies.

- **[grumpy-reviewer](https://github.com/lazy-senior-dev/grumpy-reviewer)** — the staff engineer who blocks the merge. Ten questions, a stop rule, and verdicts of `APPROVE` / `REQUEST_CHANGES` / `BLOCK`.
- **[paranoid-sre](https://github.com/lazy-senior-dev/paranoid-sre)** — asks what happens at 3 a.m. when this rolls out. `SHIP` / `HOLD` / `PAGE`. The strongest measured effect of the three.
- **[tenured](https://github.com/lazy-senior-dev/tenured)** — reads the git log, the postmortems and the ADRs, and asks whether the repository has tried this before and undone it. `NEW` / `SEEN_BEFORE` / `DO_NOT_REPEAT`.

They compose. The Grump reviews the diff, the SRE asks what it does to production, Tenured asks whether you already tried it in 2024.

Every rule maps to a **vendor-neutral** standard — MITRE CWE, OWASP, NIST SSDF, SEI CERT, CIS Benchmarks — and where no neutral identifier exists, the table says so rather than borrowing one. Releases carry SLSA build provenance, Sigstore signatures, and both CycloneDX and SPDX bills of materials.

## Why you might try one

Not because your agent misses bugs. It mostly does not.

Because right now it interrupts you about code that is fine, and when you ask it to decide, it writes you a paragraph instead of an answer. One markdown file changes both, and the second one is what turns a chat window into something you can actually gate a merge on.

```bash
npx github:lazy-senior-dev/grumpy-reviewer install
```

The benchmarks are in the repositories with the raw transcripts, the per-case tables, the failures, and the control arm that makes my numbers look worse. `npm run bench` reproduces them against your own agent. If your numbers disagree with mine, publish them — that is considerably more useful to me than a star.

---

*The three personas are Apache-2.0 and live under [lazy-senior-dev](https://github.com/lazy-senior-dev) — [grumpy-reviewer](https://lazy-senior-dev.github.io/grumpy-reviewer/), [paranoid-sre](https://lazy-senior-dev.github.io/paranoid-sre/), [tenured](https://lazy-senior-dev.github.io/tenured/). Written in a personal capacity; the views here are my own and not those of my employer. Product and company names are the trademarks of their respective owners, and their appearance in a benchmark is a measurement, not an endorsement in either direction.*
