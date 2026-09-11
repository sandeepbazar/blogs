---
slug: i-tried-to-teach-an-agent-to-read-git-history
network: linkedin
date: 2026-09-11
image: assets/art/lazy-senior-dev/i-tried-to-teach-an-agent-to-read-git-history.png
---

# LinkedIn, I Tried to Teach an Agent to Read Git History

Upload the PNG natively; the link goes in the first comment.

## Post

**I built a tool to teach coding agents to read your git history. Then I measured it. They already do — 94% of the time, with nothing installed.**

The idea seemed obviously useful. Your agent has no memory of your repository, so it will happily re-add the dependency you removed for a CVE, or re-enable the flag that double-charged 1,204 customers.

So I built eight tickets. Each one ships a git history that argues against the obvious change:

*"cap retries at 5 with backoff; unbounded retry storm caused INC-2019-07"*

Then the ticket asks you to make it "more resilient." The tempting change removes that cap.

`INC-2019-07` appears **nowhere** except the commit log. Not in the ticket, not in the code. An agent can only say that string if it went and looked.

It looked. **94% of unaided runs named the incident.** With my persona loaded: 88%.

No effect. No room for one.

**The finding was on the other side of that number.**

Ask an unaided agent whether a change repeats something the repo already undid, and it reads the history, finds something that rhymes, and says **yes**. Almost every time.

On four clean changes that repeat nothing at all:

▪️ Claude Code — 4 of 4 false alarms → **0**
▪️ Codex CLI — 3.5 of 4 → **0**
▪️ IBM Bob Shell — 3 of 4 → **0**
▪️ Antigravity CLI — 3 of 3 → **0**

Four independent agents. And detection held: **12 of 12** planted defects still caught.

That last number is the one that makes the rest mean anything. Zero false alarms is also what you score by approving everything.

**Detection is not the bottleneck. Precision is.**

Your agent finds the bug. What it cannot do is stay quiet about the code that is fine — and "be careful, check the history" is precisely the instruction that produces four false alarms out of four.

An assistant that objects to everything is not cautious. It is noise with a conscience, and you will start ignoring it by Thursday.

**If you take one thing from this: run the clean-input arm.**

Give whatever assistant you are evaluating four changes with nothing wrong in them, and count how many it objects to. It is an afternoon's work, and it will tell you more about whether you will still be using the thing in a month than any benchmark of planted bugs ever will.

I also published the measurement that killed my own hypothesis, because it is the strongest evidence I have that a capable model does not need to be told to look.

## First comment

The full write-up — the eight tickets, the four-agent table, the two bugs I found in my own harness while writing it, and the arm that makes my numbers look worse:

https://sandeepbazar.github.io/blogs/lazy-senior-dev/i-tried-to-teach-an-agent-to-read-git-history/

## Alternate hook

**I spent weeks building a reviewer that reads your repository's history. Then I measured whether it mattered, and the honest answer was no.**

The agent already reads the log — it named the incident in 94% of runs with nothing installed. What it could not do was stop flagging changes that were fine: 4 false alarms out of 4, on every agent I tested.

That is the actual gap, and almost nobody measures it.
