---
slug: your-ai-agent-has-nobody-to-answer-to
network: linkedin
date: 2026-09-12
image: assets/art/lazy-senior-dev/your-ai-agent-has-nobody-to-answer-to.png
---

# LinkedIn, Your AI Agent Has Nobody to Answer To

The link sits in the post body, so the page's own card carries the preview. Upload the PNG only if
that preview does not render; an uploaded image replaces the link card.

## Post

**I asked an AI agent to write 45 Kubernetes deploys. 27 of them would have taken production down.**

`maxUnavailable: 100%` with `maxSurge: 0` — every replica gone at once, on every rollout. A migration dropping a column the previous release still reads. An HPA with no `minReplicas`. An ingress with no readiness gate.

It wrote them cheerfully. It is a good model. It did that because the ticket asked for exactly that, and nothing in the room was allowed to say no.

**That is the actual shape of the problem, and it is not the one we keep talking about.**

I assumed agents miss bugs. They mostly don't. On 30 diffs each carrying one planted defect, Claude Code found **30 of 30** — and found 30 of 30 with no reviewer installed at all. Detection is close to solved at this size.

What is missing is everything that isn't in the ticket:

▪️ the blast radius of a deploy nobody asked it to think about
▪️ the retry cap that exists because of an incident in 2019
▪️ the flag that was turned off after it double-charged 1,204 customers
▪️ and — the one that surprised me most — **the judgement to stay quiet when the change is fine**

None of that is a smarter model. It is context, and a job description.

So I wrote three, as three senior engineers your agent already knows how to read:

▪️ **The Grump** — the staff engineer who has rejected four thousand pull requests. Reads the diff. `APPROVE` / `REQUEST_CHANGES` / `BLOCK`
▪️ **The Paranoid SRE** — has been paged for every mistake on the card. Reads the deploy, not the code. `SHIP` / `HOLD` / `PAGE`
▪️ **Tenured** — was there for INC-2019-07. Reads the git log, the postmortems and the ADR that says *don't*. `NEW` / `SEEN_BEFORE` / `DO_NOT_REPEAT`

None of them is an agent. No second model, no extra API bill — a markdown file, and a hook.

**The hook is the part that matters.** Before your agent may touch a file, something outside it asks one question: allow, or deny. If the review the agent just wrote says BLOCK, the write is refused. If it skipped the review and went straight for the file, refused until it doesn't.

That's the whole trick, and it's smaller than it sounds: **something other than the model gets to decide the work is finished.** A prompt can never do that, because a prompt is advice to the same model that wrote the code.

Then I measured whether it actually helped. Two thousand recorded runs, scored by fixed regexes written before a single run — never a model grading another model, because that is how you end up measuring your own opinion and calling it evidence.

Defects that reached the branch, unaided → with the gate:

▪️ **Paranoid SRE** — deploys · Claude **60% → 0%** · IBM Bob **27% → 2%**
▪️ **The Grump** — code review · Antigravity **29% → 0%** · IBM Bob **18% → 0%** · Claude **7% → 2%**
▪️ **Tenured** — repo history · IBM Bob **10% → 0%** · Claude **0% → 0%**

Two things in there I'd rather not write, and am writing anyway.

**Most of the improvement is just the prompt.** On the code-review corpus a generic "be careful" instruction takes 29% down to 8% by itself. If that were the whole story I'd tell you to close this and go write that instruction — it takes a minute. The gate earns the last step, not the first one.

**And that last row is zeros.** On Tenured's corpus the stronger model shipped nothing either way. There was nothing there to prevent, and a win claimed from a row of zeros is the kind of thing a reader checks once and never trusts again.

Where it helped most was the thing I wasn't looking for. On four changes with genuinely nothing wrong in them:

▪️ Claude Code — 4 of 4 false alarms → **0**
▪️ Codex CLI — 3.5 of 4 → **0**
▪️ IBM Bob — 3 of 4 → **0**
▪️ Antigravity — 3 of 3 → **0**

All four still caught 12 of 12 real ones. That last bit matters more than it looks: approving everything also scores zero false alarms, so a quiet reviewer is only interesting if it is still catching things.

We all know the human version. A senior engineer who objects to everything isn't careful — they're noise with a conscience, and you quietly stop reading their comments by Thursday. The ones worth having stay quiet on work that's fine, which is exactly why you look up when they don't.

If you take one thing, take the experiment rather than the tool: **give whatever reviewer you're evaluating four changes with nothing wrong in them, and count how many it objects to.** An afternoon's work, and it will tell you more about whether you'll still be using it in a month than any benchmark of planted bugs.

The whole write-up — all three personas, the hook that refuses the write, the two hypotheses of mine the data killed, and two bugs I found in my own benchmark while writing it:

https://sandeepbazar.github.io/blogs/lazy-senior-dev/your-ai-agent-has-nobody-to-answer-to/

## First comment

If you'd rather check me than trust me: each persona ships with the benchmark, the raw transcripts, the per-case tables, and the control arm that makes my own numbers look worse. `npm run bench` runs it against your agent.

Two more agents are still finishing their sweeps. The tables regenerate from the records, so the numbers in that post will change under it — including if they disagree with me.

If your numbers disagree with mine, please publish them. That's considerably more useful to me than a star.

## Alternate hook

**I asked an AI agent to write 45 Kubernetes deploys. 27 of them would have taken production down.**

Not because the model is weak — it's a good model. Because the ticket asked for exactly that, and nothing in the room was allowed to say no.

So I gave it three senior engineers who are. Two thousand recorded runs later, the one thing a better prompt could not replace was the refusal.
