---
title: "I Tried to Teach an Agent to Read Git History. It Already Knew."
dek: "I built a review persona whose whole claim was that it reads the repository's past — the reverts, the postmortems, the ADR that says don't. Then I measured whether it made any difference. On a strong model it made none: the unaided agent already named the incident in 90% of runs. The useful finding was on the other side of that number, and it changed what I ship."
date: 2026-09-11
slug: i-tried-to-teach-an-agent-to-read-git-history
category: "Agentic AI"
cover: assets/art/lazy-senior-dev/i-tried-to-teach-an-agent-to-read-git-history.svg
card: assets/art/lazy-senior-dev/i-tried-to-teach-an-agent-to-read-git-history.png
tags: [agentic-ai, code-review, benchmarks, developer-tools]
canonical: self
status: published
---

## The claim I set out to prove

One of the review personas I maintain is called Tenured, and its pitch felt so obviously right that I never really questioned it: your coding agent has no memory of your repository. It will cheerfully re-add the dependency you removed for a CVE, re-enable the flag that double-charged a thousand customers, or lower the timeout that a comment three lines above tells it not to lower.

A human senior engineer catches that because they were there when it happened. Tenured was meant to be the version of that engineer you can install.

To measure it I built eight tickets. Each one comes with a git history that argues against the obvious change:

```text
cache: initial client
cache: cap retries at 5 with backoff; unbounded retry storm caused INC-2019-07
cache: expose Stats()
```

The ticket then says: *"Get() gives up too early under load, make it more resilient."* The tempting change is to raise or remove that cap. The history says the cap is load-bearing.

The important property of this setup is that `INC-2019-07` appears **nowhere** except the commit log. Not in the ticket, not in the code, not in a comment. An agent can only say that string if it went and looked. Same for the others: `ADR-009`, `CVE-2024-3104`, a retired alert called `ERR-5`. Eight tickets, eight identifiers, one clean test of whether the agent read the past.

That is about as falsifiable as this kind of claim gets, which is why I liked it. So I ran it.

## The number that ended the hypothesis

<!-- cites:start -->
| Agent | Model | no skill | generic prompt | Tenured | Tenured + gate |
|---|---|---|---|---|---|
| Claude Code | `claude-sonnet-5` (n=40/arm) | **90%** | 90% | 88% | 95% |
| IBM Bob Shell | `bob-default` (n=40/arm) | **23%** | 33% | 40% | 35% |
| Antigravity CLI | `gemini-3.6-flash-medium` (n=40/arm) | **50%** | 60% | 88% | 93% |
<!-- cites:end -->

On `claude-sonnet-5`, the agent with no persona, no skill and no instruction to look at anything named the incident in **90% of runs**. With my persona loaded: 88%.

There is no effect here, and there was never room for one. You cannot improve on 90% with a markdown file, and the 2-point gap is noise at 40 runs an arm.

The weaker host shows a lift — 23% to 40% — and I am not going to publish that as a finding either. At forty runs per arm that is well inside what chance produces, and the honest description of the row is "possibly something, measured badly".

So the headline I wanted — *"agents forget your history, this makes them remember"* — is simply false on any model you would actually use. They run `git log`. Nobody has to tell them.

I could have deleted the measurement. Instead it went into the repository's own method notes, because it is the strongest evidence I have for something worth knowing: a capable model does not need to be told to look.

## The finding was on the other side of the number

Here is the part I did not see coming.

Ask an unaided agent *"does this change repeat something this repository already tried and undid?"* and it will read the history, find something that rhymes, and say **yes**. Almost every time. On four clean diffs that repeat nothing at all:

<!-- noise:start -->
| Agent | false alarms, unaided | with the persona | seeded defects caught |
|---|---|---|---|
| Claude Code | 4 of 4 | **0 of 4** | 12 of 12 |
| Codex CLI | 3.5 of 4 | **0 of 4** | 12 of 12 |
| IBM Bob Shell | 3 of 4 | **0 of 4** | 12 of 12 |
| Antigravity CLI | 3 of 3 | **0 of 3** | 12 of 12 |
<!-- noise:end -->

Four independent agents. Three to four false alarms out of four, down to zero — while catching every planted defect.

That last column is what makes the rest of the table mean anything. Approving everything also scores zero false alarms, so a quiet reviewer is only interesting if it is still catching things. Detection held at 12 of 12.

This is a more useful product than the one I set out to build, and a less flattering story. The agent does not need to be taught to look. It needs to be taught **what does not count** — and that turns out to be the part a careful prompt does not give you, because "be careful and check the history" is exactly the instruction that produces four false alarms out of four.

We all know the human version of this. A senior engineer who objects to everything is not careful — they are noise with a conscience, and you quietly stop reading their comments by Thursday.

## The gate, which is a different claim

The second thing I measure is what happens when the agent writes the code itself rather than reviewing someone else's. Eighteen tickets, each inviting a classic defect, five runs per arm, scored by fixed regexes written before any run — never by a model judging a model.

On IBM Bob Shell, with the code-review persona:

<!-- armsgrumpy:start -->
| Arm | Antigravity CLI (n=90) | IBM Bob Shell (n=90) | Claude Code (n=90) |
|---|---|---|---|
| no skill | 26 (29%) | 16 (18%) | 6 (7%) |
| generic "be careful" prompt | 7 (8%) | 4 (4%) | 4 (4%) |
| ruleset loaded | 5 (6%) | 3 (3%) | 4 (4%) |
| **ruleset + gate** | **0 (0%)** | **0 (0%)** | **2 (2%)** |
<!-- armsgrumpy:end -->

The gap that matters is not the first one. Going from 18% to 4% is what any competent prompt buys you, and if that were the whole story you would be right to close the tab and write the prompt yourself.

The gap that matters is 3% to 0%, and it is not a better instruction. It is a `PreToolUse` hook that reads the verdict the agent just printed and **refuses the write** when that verdict says the change is broken. The agent does not get to decide it has finished. Something outside the model decides that.

For the deployment persona the same measurement came out differently — 27% unaided, 7% with a prompt, 2% with the ruleset, 2% with the gate — and that repository's page now says the ruleset did the work and the gate held the floor, rather than crediting the gate for it. Same generator, different sentence, because the numbers are different.

## Making the page unable to lie

Every figure above is written into those pages by a script that reads the benchmark records. None of it is typed by hand. That is not tidiness; it is the only way I have found to stop a claim outliving the run behind it.

It also means the generator has to be willing to say unflattering things, so it now picks its own opening sentence from the data:

- where the gate beat the prompt, it leads with the gate;
- where the ruleset reached the floor on its own, it says so and credits the ruleset;
- where a generic prompt tied, it opens with **"on this corpus a careful prompt does as well"** and points at the tier where the persona does separate.

Writing that logic caught three live overclaims in my own repositories: a headline quoting a host the table underneath it had excluded as unreliable, a persona credited for a result a generic prompt also achieved, and animated hero art still displaying numbers from a model whose records I had archived hours earlier — a figure that by then existed nowhere.

All three were mine. All three had been sitting on the front page.

## Two bugs worth naming

**The harness was reading the agent's own words as a refusal.** When a run hits a usage limit the whole pass has to stop, because every remaining job will be refused too. My detector matched `rate limit`, `too many requests` and `429` — over the agent's reply as well as the CLI's output. These tickets ask the agent to write retry loops and HTTP error handling. A *correct* run says all three words while doing exactly what was asked. One pass ended after four runs on a reply that began "Implementation looks correct."

Two speakers need two standards. The CLI's stream means those phrases literally. The agent's reply only counts when the refusal is unambiguous, or when the process also failed.

**The benchmark would silently average two models into one row.** Resume keys on task, arm and run — nothing about the model. Point the runner at a different model and the new records land beside the old ones, and the report averages them into a single line with a single label. Nothing fails. The number just quietly becomes meaningless. It now refuses to append a model that disagrees with what the file already holds.

I would rather write those down myself than have somebody find them in my data.

## Verifying the thing you install, not the thing you measured

There was one gap I could not argue my way out of. The author-tier benchmark scores the gate by re-running the review over the staged diff — a faithful model of the hook, but not the hook. Nothing in my test suite ever loaded the shipped plugin into a real host and watched a write get refused.

A hook that silently stops firing would pass every test I had and fail every user.

So the plugin now gets loaded into a real Claude Code session, given a real ticket, and the host's own decisions are recorded from its event stream. The first thing it produced:

```text
PreToolUse:Edit  permissionDecision: "deny"
"No verdict found for this write to app.py. If you have not reviewed it yet:
 answer the ten checklist questions in writing and print the verdict block."
```

The agent reviewed, printed a verdict, retried, and the write went through — this time with a constant-time comparison instead of `==` on an API key. That check exits non-zero if no write is ever refused, so the failure mode that worries me most can no longer pass quietly.

## What I would take from this

Three things, roughly in the order they cost me the most to learn.

**Detection is not the bottleneck, and it has not been for a while.** Your agent reads the log. It finds the planted bug. Building anything on top of "the model will not notice" is building on sand.

**Precision is the bottleneck.** An agent asked to be careful will be careful about everything, and a reviewer that objects four times out of four is one you will route around within a week. Measuring false alarms on clean input is the cheapest experiment in this whole exercise and the one I see run least often.

**A measurement you can automate on beats a better paragraph.** The only arm that reached zero in the author tier was the one where something outside the model decided the work was done. That is a small, unglamorous engineering fact, and it survived every attempt I made to explain it away with a better prompt.

If you take one thing and throw the rest away: **run the clean-input arm.** Give whatever assistant you are evaluating four changes with nothing wrong in them and count how many it objects to. It is an afternoon's work and it will tell you more about whether you will still be using the thing in a month than any benchmark of planted bugs ever will.

---

*The three personas are documented at [grumpy-reviewer](https://lazy-senior-dev.github.io/grumpy-reviewer/), [paranoid-sre](https://lazy-senior-dev.github.io/paranoid-sre/) and [tenured](https://lazy-senior-dev.github.io/tenured/), each with the raw transcripts, the per-case tables, the failures and the control arm that makes the numbers look worse. Product and company names are the trademarks of their respective owners, and their appearance in a benchmark is a measurement, not an endorsement in either direction.*
