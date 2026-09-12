---
slug: your-ai-agent-has-nobody-to-answer-to
network: linkedin
date: 2026-09-12
image: assets/art/lazy-senior-dev/your-ai-agent-has-nobody-to-answer-to.png
---

# LinkedIn, Your AI Agent Has Nobody to Answer To

Upload the PNG natively; the link goes in the first comment.

## Post

**Your coding agent writes the change, reviews its own diff, agrees with itself, and commits. Every step in that loop is the same model. At 2 a.m. With nobody in the room.**

We spent forty years building code review around one idea: the author is the worst possible judge of their own work. Not careless — just unable to see the thing they didn't think of.

Then we handed the keyboard to something that reviews its own diffs by default.

So I built three senior engineers that live inside the agent:

▪️ **The Grump** — staff engineer, reads the diff. `APPROVE` / `REQUEST_CHANGES` / `BLOCK`
▪️ **The Paranoid SRE** — on-call, reads the deploy, not the code. `SHIP` / `HOLD` / `PAGE`
▪️ **Tenured** — was there. Reads the git log and the postmortem. `NEW` / `SEEN_BEFORE` / `DO_NOT_REPEAT`

None of them is an agent. No second model, no extra API bill. One markdown ruleset that compiles into whatever your host already reads.

**Then I measured whether any of it mattered.** 2,000 recorded runs. Agents writing real code against tickets that each invite a classic defect. Scored by fixed regexes written before any run — never a model judging a model.

Defects that reached the branch, 90 runs per arm:

▪️ **Antigravity** — 29% unaided → 8% with a careful prompt → **0% with the gate**
▪️ **IBM Bob** — 18% → 4% → **0%**
▪️ **Claude Code** — 7% → 4% → **2%**

**Read the middle number first. Most of the benefit is the prompt.** 29% to 8% is what any competent instruction buys you. If that were the whole story, you should close the tab and go write the instruction yourself.

The part a prompt cannot do is the last step.

The persona is a `PreToolUse` hook. Before your agent may run Edit, Write or Bash, it answers one question: **allow, or deny.** If the verdict the agent just printed says BLOCK, the write is refused. If it skipped the review entirely, refused until it doesn't.

**Something outside the model decides whether the work is done.** A prompt can't — a prompt is advice to the same model that wrote the code.

**And the finding I didn't expect, which I now think is the main one:**

Detection was never the problem. On 30 diffs each carrying one planted defect, Claude Code caught 30 of 30 with my reviewer — and 30 of 30 without it.

What agents are bad at is **stopping**. On clean changes with nothing wrong in them:

▪️ Claude Code — 4 of 4 false alarms → **0**
▪️ Codex CLI — 3.5 of 4 → **0**
▪️ IBM Bob — 3 of 4 → **0**
▪️ Antigravity — 3 of 3 → **0**

All four still caught 12 of 12 planted defects. That last number is what makes the rest mean anything — zero false alarms is also what you score by approving everything.

An assistant that objects to everything is not cautious. It's noise with a conscience, and you'll start ignoring it by Thursday.

**If you take one thing from this: run the clean-input arm.** Give whatever assistant you're evaluating four changes with nothing wrong in them and count how many it objects to. An afternoon's work, and it will tell you more than any benchmark of planted bugs.

I also published the measurements that killed my own hypotheses, and two bugs I found in my own harness. Those are in the write-up too.

## First comment

The full write-up — the three personas, the hook that refuses the write, the arm that makes my numbers look worse, and the two bugs I found in my own benchmark while writing it:

https://sandeepbazar.github.io/blogs/lazy-senior-dev/your-ai-agent-has-nobody-to-answer-to/

## Alternate hook

**I gave my AI coding agent a senior engineer who is allowed to say no. Across 2,000 recorded runs, that refusal was the only thing a better prompt could not replace.**

Unaided, 29% of runs shipped the defect. A careful prompt took it to 8% — most of the benefit, and you can write that prompt yourself in a minute.

The last step to 0% wasn't a better sentence. It was a hook that refuses the write until the agent's own review passes.
