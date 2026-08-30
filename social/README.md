<!-- SPDX-FileCopyrightText: 2026 Sandeep Bazar -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# social

Ready-to-paste announcement copy, filed the way [posts](../posts/) and
[assets](../assets/) are — by the project the writing belongs to.

```
social/<collection>/YYYY-MM-DD-<slug>-<network>.md
```

Nothing here is rendered and nothing here posts anything anywhere. It is
checked by the build anyway, because the one failure mode that matters —
pasting a dead link into a feed — is not something you find out about from
your own machine.

## Front matter

```yaml
---
slug: three-agents-one-server-same-seven-walls   # the post being announced
network: linkedin
date: 2026-08-30
image: assets/art/<collection>/<slug>.png        # optional; what to upload
---
```

The build fails if `slug` names no published post, if that post lives in a
different collection than the file, or if `image` does not resolve.

## House style

Keep it **short**. The write-up is the long version; the post exists to earn
the click, not to replace it.

- Open with the result, in bold, in one sentence. The surprising number goes
  first, not the setup.
- Bold the two or three phrases someone should catch while scrolling past.
- One concrete detail beats three abstract claims.
- Links go in the **first comment**, not the body.
- Upload the image natively — LinkedIn gives an uploaded image far more of
  the feed than a link preview.

Each file carries the post, the first comment, and an alternate hook, so
there is a choice to make at posting time rather than a draft to write.
