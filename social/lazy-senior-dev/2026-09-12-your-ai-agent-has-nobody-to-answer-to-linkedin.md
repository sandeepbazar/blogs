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

Plain text, ready to paste. No markdown: LinkedIn renders asterisks and backticks literally.
Attach share-vertical.gif (1080x1350). The link is in the body; the first comment carries the rest.

```
I asked an AI agent to write 45 Kubernetes deploys.

27 of them would have taken production down.

maxUnavailable: 100%, with maxSurge: 0. A migration dropping a column the previous release still reads. It wrote them cheerfully — it is a good model. It did that because the ticket asked for exactly that, and nothing in the room was allowed to say no.

That is the real problem, and it is not the one we keep talking about.

Your agent writes the change, reviews its own diff, agrees with itself, and commits. Every step is the same model.

So I gave it three senior engineers who are allowed to say no:

🔍 The Grump — reads the diff
🚨 The Paranoid SRE — reads the deploy, not the code
📜 Tenured — reads the git log and the postmortem

Each is one markdown file plus a hook. Before the agent may touch a file, something outside it answers one question: allow, or deny.

2,000 recorded runs. Defects that reached the branch, unaided → with the gate:

▪️ Deploys — 60% → 0%
▪️ Code review — 29% → 0%
▪️ Repository history — 10% → 0%

Two things I would rather not write:

Most of that is just the prompt. A generic "be careful" takes 29% to 8% on its own. The gate earns the last step, not the first.

And detection was never the problem. 30 of 30 planted bugs found with my reviewer — and 30 of 30 without it. What agents are bad at is stopping. On four changes with nothing wrong in them: 4 false alarms, down to 0, still catching 12 of 12 real ones.

A senior engineer who objects to everything is not careful. They are noise with a conscience, and you stop reading them by Thursday.

Full write-up, all the numbers, and the two hypotheses of mine the data killed:
https://sandeepbazar.github.io/blogs/lazy-senior-dev/your-ai-agent-has-nobody-to-answer-to/

#AgenticAI #AICodeReview #DeveloperTools #Kubernetes #SRE
```

## First comment

```
The three, each one markdown file — no second model, no extra API bill:

🔍 The Grump, code review → https://lazy-senior-dev.github.io/grumpy-reviewer/
🚨 The Paranoid SRE, deploys → https://lazy-senior-dev.github.io/paranoid-sre/
📜 Tenured, repository memory → https://lazy-senior-dev.github.io/tenured/

Install one:
npx github:lazy-senior-dev/grumpy-reviewer install

Works in Claude Code, Codex, Copilot CLI, Cursor, Windsurf, IBM Bob, Antigravity and 7 more. Also a GitHub Action, so it reviews human pull requests too.

If you would rather check me than trust me: each ships with the benchmark, the raw transcripts, the per-case tables, and the control arm that makes my own numbers look worse. npm run bench runs it against your own agent.

Two more agents are still finishing their sweeps. The tables regenerate from the records, so those numbers will move — including if they end up disagreeing with me.
```

## Alternate hook

```
Detection was never the problem.

I gave four AI coding agents 30 diffs, each with one planted bug. They found 30 of 30 — and 30 of 30 with no reviewer installed at all.

Then I gave them four changes with nothing wrong in them. They raised 4 false alarms out of 4.

An assistant that objects to everything is not cautious. It is noise with a conscience, and you stop reading it by Thursday.
```
