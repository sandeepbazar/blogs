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

It was about two in the morning when I noticed what my coding agent had actually been doing all evening.

It wrote a change. Then it reviewed the change. Then it decided the change was good. Then it wrote the file.

Every step in that loop was the same model, agreeing with itself, with nobody else in the room.

We spent forty years building code review around the opposite instinct — that the author is the worst possible judge of their own work. Not because they are careless, but because they cannot see the thing they never thought of. That is the whole reason someone else reads it.

Then we handed the keyboard to something that reviews its own diffs by default, and we called it productivity.

So I tried giving it a colleague. Three, actually:

▪️ **The Grump** — the staff engineer who has rejected four thousand pull requests. Reads the diff. `APPROVE` / `REQUEST_CHANGES` / `BLOCK`
▪️ **The Paranoid SRE** — has been paged for every mistake on the card. Doesn't read your code, reads your deploy. `SHIP` / `HOLD` / `PAGE`
▪️ **Tenured** — was there in 2024. Reads the git log and the postmortem, and asks whether you already tried this. `NEW` / `SEEN_BEFORE` / `DO_NOT_REPEAT`

None of them is an agent. No second model, no extra API bill — just a markdown file your existing agent already knows how to read.

Then I did the part I was dreading, which was checking whether any of it helped.

Two thousand recorded runs. Agents writing real code against tickets that quietly invite a classic mistake. Every result scored by fixed regexes written before a single run — never a model grading another model, because that is how you end up measuring your own opinion.

Defects that reached the branch, 90 runs per arm:

▪️ **Antigravity** — 29% on its own → 8% with a careful prompt → **0% with the gate**
▪️ **IBM Bob** — 18% → 4% → **0%**
▪️ **Claude Code** — 7% → 4% → **2%**

Look at the middle number before the last one, because it is the uncomfortable one. **Most of the benefit is just the prompt.** Going from 29% to 8% is what any decent instruction buys you, and if that were the whole story I would tell you to close this and go write that instruction yourself. It would take a minute.

What a prompt cannot do is the last step.

The persona runs as a hook. Before the agent is allowed to touch a file, something outside it asks one question: allow, or deny. If the review the agent just wrote says BLOCK, the write is refused. If it skipped the review and went straight for the file, refused until it doesn't.

That is the entire trick, and it is smaller than it sounds. **Something other than the model gets to decide the work is finished.** A prompt can never do that, because a prompt is advice to the same model that wrote the code.

Then came the finding I did not want, and now think is the important one.

Detection was never the problem. On 30 diffs each carrying one planted bug, Claude Code found 30 of 30 with my reviewer installed — and 30 of 30 without it. These models are not bad at noticing that an unchecked lookup will blow up in production.

What they are bad at is **stopping**.

Ask one whether a change looks risky and it will find you something. On four changes with genuinely nothing wrong in them:

▪️ Claude Code — 4 of 4 false alarms → **0**
▪️ Codex CLI — 3.5 of 4 → **0**
▪️ IBM Bob — 3 of 4 → **0**
▪️ Antigravity — 3 of 3 → **0**

And all four still caught 12 of 12 real ones. That last bit matters more than it looks: approving everything also scores zero false alarms, so a quiet reviewer is only interesting if it is still catching things.

We all know the version of this person. A senior engineer who objects to everything isn't careful — they're noise with a conscience, and you quietly stop reading their comments by Thursday. The ones worth having are the ones who stay quiet on work that is fine, which is exactly why you look up when they don't.

If you take one thing from this, take the experiment rather than the tool: **give whatever reviewer you are evaluating four changes with nothing wrong in them, and count how many it objects to.** It is an afternoon's work and it will tell you more about whether you will still be using it in a month than any benchmark of planted bugs.

I wrote the whole thing up, including the two hypotheses of mine the data killed and the two bugs I found in my own benchmark while writing it:

https://sandeepbazar.github.io/blogs/lazy-senior-dev/your-ai-agent-has-nobody-to-answer-to/

## First comment

If you want to check me rather than trust me: each persona ships with the benchmark, the raw transcripts, the per-case tables, and the control arm that makes my own numbers look worse. `npm run bench` runs it against your agent.

If your numbers disagree with mine, please publish them. That is considerably more useful to me than a star.

## Alternate hook

I spent weeks building a reviewer that reads your repository's history — the reverts, the postmortems, the ADR that says *don't*. Then I measured whether it changed anything, and the honest answer was no.

The agent already reads the log. It named the incident in 90% of runs with nothing installed at all.

What it could not do was stop flagging changes that were fine: four false alarms out of four, on every agent I tested. That turned out to be the real gap, and almost nobody measures it.
