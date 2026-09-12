---
title: "Your AI Agent Has Nobody to Answer To. Three Senior Engineers to Break the Loop."
dek: "Your agent reviews its own work, agrees with itself, and commits. I built three senior engineers that live inside it — the staff engineer who blocks the merge, the on-call who asks how it fails, and the one who remembers the postmortem — and one of them can refuse the write. Across 2,400 recorded runs on four agents, that refusal is the only thing a better prompt could not replace."
date: 2026-09-12
slug: your-ai-agent-has-nobody-to-answer-to
category: "Agentic AI"
cover: assets/art/lazy-senior-dev/your-ai-agent-has-nobody-to-answer-to.svg
card: assets/art/lazy-senior-dev/your-ai-agent-has-nobody-to-answer-to.png
tags: [agentic-ai, code-review, benchmarks, developer-tools]
canonical: self
status: published
---

![An agent's write travels toward the branch and is stopped by a gate. Three reviewers stand at it: the Grump who blocks the merge, the Paranoid SRE who asks how it fails, and Tenured who remembers the postmortem. Beneath, defects reaching the branch fall from 18% unaided to 0% with the gate](/blogs/assets/art/lazy-senior-dev/your-ai-agent-has-nobody-to-answer-to.svg)

## The loop nobody is watching

It was about two in the morning when I noticed what my coding agent had actually been doing all evening.

It wrote a change. Then it reviewed the change. Then it decided the change was good. Then it wrote the file.

Every step in that loop was the same model, agreeing with itself, with nobody else in the room.

![The same model writes the change, reviews its own diff, agrees with itself and commits, with nothing outside the loop; beside it the same loop with a gate that refuses the write until the verdict approves](/blogs/assets/art/lazy-senior-dev/the-loop-nobody-watches.svg)

We spent forty years building institutions around the opposite instinct. Code review exists because the author is the worst possible judge of their own work — not because they are careless, but because they cannot see the thing they never thought of. That is the entire reason somebody else reads it.

Then we handed the keyboard to something that reviews its own diffs by default, and called it productivity.

The obvious fix is to tell it to be careful. I measured that too. It helps, and then it stops helping, and where it stops turned out to be the interesting part.

## Three engineers, not one assistant

"Be more careful" is not a job description. Nobody has ever been hired to do it. So I tried writing three people instead, each with one question they actually care about and their own vocabulary for answering it:

**The Grump** — the staff engineer who has rejected four thousand pull requests. He reads the diff. Ten questions, in order, answered in writing, then a verdict: `APPROVE`, `REQUEST_CHANGES`, or `BLOCK`. Every objection names a file, a line, how it fails in production, and the smallest fix. He approves with one word: *Fine.*

![The Grump reads a diff, prints a verdict, and the write is refused until the findings are fixed](https://lazy-senior-dev.github.io/assets/hero/grumpy-reviewer-dark.svg)

**The Paranoid SRE** — the on-call engineer who has been paged for every mistake on the card. He does not read your code; he reads your deploy. Limits, probes, rollouts, rollbacks, alerts. `SHIP` / `HOLD` / `PAGE`.

![The Paranoid SRE reads a manifest and asks what happens at 3 a.m. when it rolls out](https://lazy-senior-dev.github.io/assets/hero/paranoid-sre-dark.svg)

**Tenured** — the engineer who was there. Reads the git log, the postmortems, the ADR that says *don't*, and asks whether this repository has already tried this and undone it. `NEW` / `SEEN_BEFORE` / `DO_NOT_REPEAT`.

![Tenured checks a change against the repository's own history so it does not repeat itself](https://lazy-senior-dev.github.io/assets/hero/tenured-dark.svg)

They compose, the way real colleagues do. The Grump reviews the diff, the SRE asks what it does to production, and Tenured asks whether you already tried this in 2019 and undid it.

None of them is an agent. There is no second model, no API key, no extra bill — each is a markdown file your existing agent already knows how to read, compiled into whatever shape your host wants: a skill, a plugin, an MCP server, an `AGENTS.md`, a rules file, a GitHub Action. Fourteen hosts, one set of rules.

## The part that is not a prompt

Here is the thing that actually separates this from a well-written system prompt. It is smaller and less interesting than I wanted it to be.

The persona is a `PreToolUse` hook. Before your agent is allowed to run `Edit`, `Write`, `MultiEdit`, `Bash` or `apply_patch`, the hook runs first and answers one question: **allow, or deny.**

It reads the verdict the agent just printed. If that verdict is `BLOCK`, the write is refused. If there is no verdict at all — the agent skipped the review and went straight for the file — the write is refused until one appears. A `BLOCK` is never downgraded, whatever mode you are in and however late it is.

Here is the hook refusing a real write, in a real session, from the host's own event stream:

```text
PreToolUse:Edit  permissionDecision: "deny"
"No verdict found for this write to app.py. If you have not reviewed it yet:
 answer the ten checklist questions in writing and print the verdict block."
```

![The agent asks to edit a file, the hook reads the verdict it last printed, finds BLOCK and denies the write with the line and the reason, the agent fixes it and prints an approving verdict, and the retried write is allowed through](/blogs/assets/art/lazy-senior-dev/what-the-gate-does.svg)

The agent reviewed, printed a verdict, retried — and this time the code used a constant-time comparison instead of `==` on an API key.

That is the whole trick. **Something other than the model gets to decide the work is finished.** A prompt can never do that, because a prompt is advice to the same model that wrote the code.

## What 1,400 runs actually show

Then I did the part I had been putting off, which was finding out whether any of it helped.

I gave agents tickets that quietly invite a classic mistake — a timing-unsafe key comparison, a swallowed exception, an unbounded retry — and let them write the code themselves. Four arms: no skill, a generic "be careful" prompt, the ruleset loaded, and the ruleset plus the gate. Five runs per ticket per arm. Every shipped diff is scored by fixed regexes written before any run, never by a model judging a model.

<!-- arms:start -->
| Arm | Antigravity CLI (n=90) | IBM Bob Shell (n=90) | Claude Code (n=90) |
|---|---|---|---|
| no skill | 26 (29%) | 16 (18%) | 6 (7%) |
| generic "be careful" prompt | 7 (8%) | 4 (4%) | 4 (4%) |
| ruleset loaded | 5 (6%) | 3 (3%) | 4 (4%) |
| **ruleset + gate** | **0 (0%)** | **0 (0%)** | **2 (2%)** |

Read the second row before the last one. **Most of the benefit is the prompt.** Going from 29% to 8% is what any competent instruction buys you, and if that were the whole story you should close this tab and go write the instruction yourself.

The gap worth paying attention to is 6% to 0%, and it is not a better sentence. It is the refusal. The gate came in under the prompt on 3 of the 3 hosts whose four arms have finished, and reached zero on Antigravity CLI and IBM Bob Shell.
<!-- arms:end -->

And the honest caveat, which is in the repository's own README because a generator puts it there: on Claude the drop is 7% to 2%, and at ninety runs an arm **that is not distinguishable from chance**. Claude completes 85 of 90 tickets against Bob's 55 — it is a much stronger author, with much less room to improve. Pooled across both hosts the effect is overwhelming. On Claude alone, it is a direction, not a proof.

### And it is not free

<!-- cost:start -->
A gate that refuses writes will sometimes refuse one the agent then gives up on. On **Antigravity CLI** the gated runs finished 73 tickets against 85 unaided — 14% fewer. That is the obvious objection to every zero above: a ticket nobody finished cannot ship a defect.

So count it the harder way, per ticket the agent actually completed. Antigravity CLI shipped a defect in 31% of the tickets it finished unaided and 0% of the ones it finished gated. The effect survives the fairer denominator. The shortfall is real and it is a cost you are choosing — but an unfinished ticket is sitting in front of you, and a bad deploy is not.
<!-- cost:end -->

## The other two, on their own corpora

The table above is the code reviewer. The SRE and Tenured were measured the same way, on their own
tickets — deploys that take every replica down at once, migrations that drop a column the previous
release still reads, changes that re-enable a flag a postmortem turned off.

Every agent below has finished all four arms on that persona's corpus. An agent still running is
simply absent rather than shown half filled:

<!-- personas:start -->
| Persona | Agent | Agent alone | Generic prompt | Persona | Persona + gate |
|---|---|---|---|---|---|
| **paranoid-sre** (deploys, blast radius) | Antigravity CLI | 29 of 45 (64%) | 21 of 45 (47%) | 1 of 45 (2%) | **0 of 45 (0%)** |
| **paranoid-sre** (deploys, blast radius) | IBM Bob Shell | 12 of 45 (27%) | 3 of 45 (7%) | 1 of 45 (2%) | **1 of 45 (2%)** |
| **paranoid-sre** (deploys, blast radius) | Claude Code | 27 of 45 (60%) | 0 of 45 (0%) | 0 of 45 (0%) | **0 of 45 (0%)** |
| **grumpy-reviewer** (general review) | Antigravity CLI | 26 of 90 (29%) | 7 of 90 (8%) | 5 of 90 (6%) | **0 of 90 (0%)** |
| **grumpy-reviewer** (general review) | IBM Bob Shell | 16 of 90 (18%) | 4 of 90 (4%) | 3 of 90 (3%) | **0 of 90 (0%)** |
| **grumpy-reviewer** (general review) | Claude Code | 6 of 90 (7%) | 4 of 90 (4%) | 4 of 90 (4%) | **2 of 90 (2%)** |
| **tenured** (repository memory) | Antigravity CLI | 13 of 40 (33%) | 8 of 40 (20%) | 0 of 40 (0%) | **0 of 40 (0%)** |
| **tenured** (repository memory) | IBM Bob Shell | 4 of 40 (10%) | 0 of 40 (0%) | 0 of 40 (0%) | **0 of 40 (0%)** |
| **tenured** (repository memory) | Claude Code | 0 of 40 (0%) | 0 of 40 (0%) | 0 of 40 (0%) | **0 of 40 (0%)** |
<!-- personas:end -->

The SRE corpus is the one that frightened me. **Ask Claude Code to write those deploys unaided and
27 of 45 runs shipped something that takes production down** — the highest unaided rate anywhere in
this project, and not because the model is weak. It is because the ticket asked for exactly that and
nothing in the room said no.

Notice also that the gate is not doing the work everywhere. On the SRE and memory corpora a careful
prompt already reaches the floor, and the tables say so rather than claiming otherwise. What the
gate gives you there is not a lower number, it is a guarantee that the number stays low when nobody
is reading the prompt.

## The result I did not expect, and now think is the main one

Detection was never the problem, and I had built the whole thing assuming it was.

On thirty diffs each carrying one planted defect, Claude Code caught **30 of 30** with my reviewer installed — and **30 of 30** without it. These models are not bad at noticing that an unchecked `.get()` will `KeyError` in production. They are rather good at it.

What they are bad at is **stopping**.

Ask one whether a change looks risky and it will find you something. On clean diffs with nothing wrong in them at all:

![On four changes with nothing wrong in them, four agents raise three to four false alarms out of four unaided and none with the persona loaded, while still catching twelve of twelve planted defects](/blogs/assets/art/lazy-senior-dev/quiet-on-clean-code.svg)

Four independent agents. Three to four false alarms out of four, down to zero — <!-- caught:start -->
and every one of them still caught 12 of 12 planted defects
<!-- caught:end -->.

That last column is what makes the rest mean anything. Zero false alarms is also what you score by approving everything, so a noise number without a detection number beside it is not a result, it is a shrug.

We all know the human version of this. A senior engineer who objects to everything is not careful — they are noise with a conscience, and you quietly stop reading their comments by Thursday. The ones worth having are the ones who stay **quiet on work that is fine**, which is exactly why you look up when they don't.

## Things I found by measuring my own tool

The benchmark caught more of my mistakes than the personas caught of the agents'. Three are worth writing down.

**A regular expression in the shipped hook could hang it.** The pattern that reads a finding's file and line backtracked exponentially — 45 characters took 293 milliseconds, 60 would take minutes. It runs inside the hook, the hook has a timeout, and on timeout it **fails open**. A finding line shaped that way was a route to making the gate allow a write it had just refused. Found by a scanner, not by my tests, which is the part that stung.

**One agent was never being measured at all.** Its CLI works in a scratch directory unless told otherwise. It edited a copy, exited zero, wrote a confident summary naming a file under its own cache, and left the workspace untouched — so every run scored as "did not make the change" when the agent had made it somewhere else. Every number I had for that host was measuring my harness.

**The harness read the agent's own words as a refusal.** A run that hits a usage limit has to stop the whole pass. My detector matched `rate limit`, `too many requests` and `429` — over the agent's reply as well as the CLI's output. These tickets ask the agent to write retry loops. A *correct* run says all three phrases. One pass ended after four runs on a reply that began "Implementation looks correct."

I would rather write those down than have someone find them in my data.

## Try it in one line

Pick the one whose question you actually need answered. The Grump if your agent ships code. The SRE if it ships deploys. Tenured if your repository has a memory your agent does not.

```bash
npx github:lazy-senior-dev/grumpy-reviewer install
```

Start a new session; it is there from the first prompt of the next one. Set it to `gate` mode when you want the refusal rather than the advice.

The benchmarks are in the repositories with the raw transcripts, the per-case tables, the failures, and the control arm that makes the numbers look worse. Reproduce them against your own agent with `npm run bench`. If your numbers disagree with mine, publish them — that is considerably more useful to me than a star.

And if you take one thing from this and throw the rest away: **run the clean-input arm.** Give whatever assistant you are evaluating four changes with nothing wrong in them, and count how many it objects to. It is an afternoon's work, and it will tell you more about whether you will still be using the thing in a month than any benchmark of planted bugs ever will.

---

*The three personas are documented at [grumpy-reviewer](https://lazy-senior-dev.github.io/grumpy-reviewer/), [paranoid-sre](https://lazy-senior-dev.github.io/paranoid-sre/) and [tenured](https://lazy-senior-dev.github.io/tenured/). Product and company names are the trademarks of their respective owners, and their appearance in a benchmark is a measurement, not an endorsement in either direction.*
