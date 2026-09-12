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

It was about two in the morning when I noticed what my coding agent had been doing all evening.

It wrote a change. Then it reviewed the change. Then it decided the change was good. Then it wrote the file.

Every step in that loop was the same model, agreeing with itself, with nobody else in the room.

We spent forty years building code review around the opposite instinct — that the author is the worst possible judge of their own work. Not because they're careless, but because they can't see the thing they never thought of. That's the entire reason somebody else reads it.

Then we handed the keyboard to something that reviews its own diffs by default, and called it productivity.

So I tried giving it colleagues. Three of them:

▪️ **The Grump** — the staff engineer who has rejected four thousand pull requests. Reads the diff.
▪️ **The Paranoid SRE** — has been paged for every mistake on the card. Doesn't read your code, reads your deploy.
▪️ **Tenured** — was there in 2024. Reads the git log and the postmortem, and asks whether you already tried this.

None of them is an agent. No second model, no extra API bill — a markdown file your existing agent already knows how to read.

Then I did the part I'd been putting off: checking whether any of it helped.

Two thousand recorded runs. Agents writing real code against tickets that quietly invite a classic mistake. Every result scored by fixed regexes written before a single run — never a model grading another model, because that's how you end up measuring your own opinion and calling it evidence.

Each persona has its own corpus, because "did it write a bug" means something different for a diff, a deploy, and a change that contradicts your own history. Defects that reached the branch, unaided and then with the gate:

▪️ **Paranoid SRE** — deploys · Claude **60% → 0%** · IBM Bob **27% → 2%**
▪️ **The Grump** — code review · Antigravity **29% → 0%** · IBM Bob **18% → 0%** · Claude **7% → 2%**
▪️ **Tenured** — repo history · IBM Bob **10% → 0%** · Claude **0% → 0%**

**That first line is the one that unsettled me.** Ask Claude Code to write 45 Kubernetes deploys with nothing watching, and **27 of them shipped something that takes production down.** `maxUnavailable: 100%`. A migration dropping a column the previous release still reads. It wrote them cheerfully — not because the model is weak, but because the ticket asked for exactly that and nothing in the room said no.

And read that last line too, because it's the honest one: on Tenured's corpus Claude shipped nothing either way. There was nothing there for a reviewer to prevent, and I'm not going to claim a win from a row of zeros.

Now the uncomfortable part, which the full tables make obvious. **Most of that improvement is just the prompt.** On the code-review corpus, a generic "be careful" instruction takes 29% down to 8% on its own — and if that were the whole story I'd tell you to close this and go write that instruction yourself. It'd take a minute.

What a prompt can't do is the last step.

The persona runs as a hook. Before the agent may touch a file, something outside it asks one question: allow, or deny. If the review the agent just wrote says BLOCK, the write is refused. If it skipped the review and went straight for the file — refused until it doesn't.

That's the whole trick, and it's smaller than it sounds. **Something other than the model gets to decide the work is finished.** A prompt never can, because a prompt is advice to the same model that wrote the code.

I'll be honest about where it doesn't help, because the tables are in the post either way: on two of the three corpora, a careful prompt already reaches the floor and the gate adds nothing to the number. What it adds there is that the number stays low when nobody's reading the prompt.

**Then came the finding I didn't want, and now think is the important one.**

Detection was never the problem. On 30 diffs each carrying one planted bug, Claude Code found 30 of 30 with my reviewer installed — and 30 of 30 without it. These models are not bad at spotting that an unchecked lookup will blow up in production.

What they're bad at is **stopping**.

Ask one whether a change looks risky and it will find you something. On four changes with genuinely nothing wrong in them:

▪️ Claude Code — 4 of 4 false alarms → **0**
▪️ Codex CLI — 3.5 of 4 → **0**
▪️ IBM Bob — 3 of 4 → **0**
▪️ Antigravity — 3 of 3 → **0**

All four still caught 12 of 12 real ones. That last bit matters more than it looks: approving everything also scores zero false alarms, so a quiet reviewer is only interesting if it's still catching things.

We all know the human version of this. A senior engineer who objects to everything isn't careful — they're noise with a conscience, and you quietly stop reading their comments by Thursday. The ones worth having stay quiet on work that's fine, which is exactly why you look up when they don't.

If you take one thing, take the experiment rather than the tool: **give whatever reviewer you're evaluating four changes with nothing wrong in them, and count how many it objects to.** An afternoon's work, and it'll tell you more about whether you'll still be using it in a month than any benchmark of planted bugs.

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
