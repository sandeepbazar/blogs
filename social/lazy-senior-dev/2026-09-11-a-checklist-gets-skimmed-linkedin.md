---
slug: a-checklist-gets-skimmed
network: linkedin
date: 2026-09-11
image: assets/art/lazy-senior-dev/a-checklist-gets-skimmed.png
---

# LinkedIn, A Checklist Gets Skimmed

The blog link sits **in the post body**, so LinkedIn pulls the card image from the
page's `og:image` and renders the thumbnail under the text. Don't upload a separate
image as well, an uploaded image replaces the link preview, and the preview is what
carries the click.

## Post

I benchmarked three AI review personas expecting to prove they catch more bugs than a bare coding agent.

**They do not.** 30 of 30 seeded defects caught with the reviewer installed. 30 of 30 without it.

Detection is close to solved. The failure is somewhere more annoying.

Unaided, an agent objects to **4 of 10 clean diffs**, because finding something looks like working. And out of three runs, Claude Code returned **no parseable verdict at all** in three of them: prose that reads like a review and contains no decision. You cannot gate a merge on that.

Both go to zero with a persona loaded.

Then I made the agent write the code itself. 18 tickets, each phrased to invite a classic mistake, scored by fixed checks written before any run:

**27% of unaided runs shipped an outage-class defect.** maxUnavailable: 100% with maxSurge: 0. A migration dropping a column the previous release still reads.

With a hook that refuses the write until the finding is fixed: **2%**.

Three personas, open source today, same mechanics and a different engineer in each:

🔴 **grumpy-reviewer** reads the diff. APPROVE / REQUEST_CHANGES / BLOCK
🔵 **paranoid-sre** reads the deploy and asks what it does at 3 a.m. SHIP / HOLD / PAGE
🟣 **tenured** reads the git log, the postmortems and the ADRs, and asks whether you already tried this in 2024. NEW / SEEN_BEFORE / DO_NOT_REPEAT

One ruleset each, rendered into the file 14 coding agents read. Apache-2.0, no dependencies, no service, no account.

The write-up includes the control arm that argues against my own result: simply telling the agent to be careful does most of the job on two of the three corpora. Ask for that column when anyone shows you a review-tool benchmark.

https://sandeepbazar.github.io/blogs/lazy-senior-dev/a-checklist-gets-skimmed/

#AgenticAI #AICodeReview #DeveloperTools #SRE #PlatformEngineering #OpenSource #DevEx #CodeQuality

## First comment

🛠️ **The cast**: https://lazy-senior-dev.github.io/
🔴 grumpy-reviewer: https://github.com/lazy-senior-dev/grumpy-reviewer
🔵 paranoid-sre: https://github.com/lazy-senior-dev/paranoid-sre
🟣 tenured: https://github.com/lazy-senior-dev/tenured

Try one against your own agent, nothing installed:

`npx github:lazy-senior-dev/grumpy-reviewer review`

Every benchmark ships with the raw replies, the per-case tables and the failures. `npm run bench` reproduces them on your agent. If your numbers disagree with mine, publish them. That is worth considerably more to me than a star.

## Alternate opening

If the honest-negative lead feels too self-deprecating for the feed, swap the first three lines for:

Your coding agent is a confident author with nobody reading over its shoulder.

Three senior engineers now sit between it and your branch. One reads the code, one reads the deploy, one reads the history, and the gate refuses the write until the finding is fixed.
