<!-- SPDX-FileCopyrightText: 2026 Sandeep Bazar -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# posts

Every post is one markdown file, filed in the folder for the **project, repo or
theme it was written about** — so that everything on one subject reads as a
series instead of a date-sorted pile. The build refuses a file that sits loose
in `posts/` or in a folder it does not recognise, which is what keeps this
honest six months from now.

The folder is organisation only. Nothing in a URL, a card or a feed changes when
a post moves: pages are published at `/blogs/<slug>/`, and `slug` lives in the
front matter.

| Folder | What goes in it | Also lives at |
|---|---|---|
| [`ocm-mcp-server/`](ocm-mcp-server/) | The guardrailed MCP control plane for Kubernetes fleets — architecture, evaluations, security lessons | [repo](https://github.com/ocm-mcp-server/ocm-mcp-server) · [docs](https://ocm-mcp-server.github.io/) |
| [`fusion-mcp/`](fusion-mcp/) | Conversational and agentic operations on IBM Fusion, via kubernetes-mcp, Fusion MCP and IBM BOB | — |
| [`ibm-fusion/`](ibm-fusion/) | The IBM Fusion platform itself — storage, OpenShift Virtualization, VMware migration, GPUs | — |
| [`research-and-life/`](research-and-life/) | Qualitative research, and the writing that is not about infrastructure | — |

## The index

| Date | Post | Category | Where it lives |
|---|---|---|---|
| 2026-08-31 | [Why Concurrent Fan-Out Benchmarks at 1.2x on Localhost](ocm-mcp-server/2026-08-31-why-fan-out-measures-1-2x-on-localhost.md) | Kubernetes & MCP | `ocm-mcp-server/` |
| 2026-08-30 | [Three Agents, One Server, and the Same Seven Walls](ocm-mcp-server/2026-08-30-three-agents-one-server-same-seven-walls.md) | Agentic AI | `ocm-mcp-server/` |
| 2026-08-01 | [Your MCP Server Is a Security Boundary, Not an API Wrapper](ocm-mcp-server/2026-08-01-mcp-server-is-a-security-boundary.md) | Kubernetes & MCP | `ocm-mcp-server/` |
| 2026-07-29 | [Can an AI Agent Take the 2 A.M. Page?](ocm-mcp-server/2026-07-29-can-an-ai-agent-take-the-2am-page.md) | Agentic AI | `ocm-mcp-server/` |
| 2026-02-08 | [Bringing Agentic AI to IBM Fusion Fleet](fusion-mcp/2026-02-08-agentic-ai-ibm-fusion-fleet.md) | IBM Fusion | `fusion-mcp/` |
| 2026-01-30 | [IBM Fusion + IBM Bob + Kubernetes-MCP: End-to-End "Conversational Ops"](fusion-mcp/2026-01-30-ibm-fusion-bob-kubernetes-mcp.md) | IBM Fusion | `fusion-mcp/` |
| 2026-01-07 | [Breaking the AI Platform Myth](ibm-fusion/2026-01-07-breaking-the-ai-platform-myth.md) | IBM Fusion | `ibm-fusion/` |
| 2025-12-18 | [Elevating Proactive Kubernetes Operations on IBM Fusion Using AI](fusion-mcp/2025-12-18-proactive-kubernetes-operations-with-ai.md) | Agentic AI | `fusion-mcp/` |
| 2025-12-14 | [What "Travelling" Really Means to a 7-Year-Old](research-and-life/2025-12-14-what-travelling-means-to-a-7-year-old.md) | Research & Life | `research-and-life/` |
| 2025-12-10 | [Bringing Agentic AI to IBM Fusion: How Kubernetes-MCP Transforms Fusion Operations](fusion-mcp/2025-12-10-agentic-ai-ibm-fusion-kubernetes-mcp.md) | IBM Fusion | `fusion-mcp/` |
| 2024-08-22 | [Seamless Virtual Machines Migration: VMware to IBM Fusion with OpenShift MTV](ibm-fusion/2024-08-22-vmware-to-fusion-migration-with-mtv.md) | IBM Fusion | `ibm-fusion/` |
| 2024-07-30 | [Unified Mastery: Bridging Virtual Machines and Containers with IBM Fusion](ibm-fusion/2024-07-30-unified-mastery-vms-and-containers.md) | IBM Fusion | `ibm-fusion/` |
| 2024-02-09 | [IBM Storage Fusion HCI and IBM Cloud Satellite Integration](ibm-fusion/2024-02-09-fusion-hci-cloud-satellite-integration.md) | IBM Fusion | `ibm-fusion/` |

## Adding one

Front matter, then the body — the full field reference is in the
[repo README](../README.md#adding-a-post). Two rules worth repeating here:

- **Pick the folder by subject, not by category.** `category` colours the chip
  on the site and is one of four fixed values; the folder says which project the
  writing belongs to. A Fusion post about the MCP work is `category: "IBM Fusion"`
  in `fusion-mcp/`, and that is not a contradiction.
- **A new folder is a code change.** Add it to `COLLECTIONS` in `build.py` with a
  one-line description, or the build will not accept posts filed there.
- **The art moves with the post.** Covers and social cards are filed the same
  way, under `assets/covers/<collection>/` and `assets/art/<collection>/`; see
  [`assets/README.md`](../assets/README.md). Re-filing a post means re-filing its
  art, and the build says so if you forget.
