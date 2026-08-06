# flightlab-theme-5 (deploy payload)

These are the files uploaded to the Shopify theme **flightlab-theme-5**.

`sections/cinematic-home.liquid` is a three-way merge, not a plain copy:

- **base** — `cinematic-home.liquid` at commit 6d5960b, which is what
  theme-5 in Shopify was built from (its `assets/fl-home.css` is
  byte-identical to that commit, md5 f721946a2c8ebb71119f8c27a632ee94).
- **theirs** — theme-5's live section, which reworked the bag portal into
  `bagcap` and was never committed here.
- **ours** — the theme-4 work on this branch: the drawn A, the restored
  Discraft models, and the ~12% lift.

The merge applied cleanly with no conflicts, so both sides survive. Pull
theme-5 down before regenerating this file, or the bagcap work is lost —
it exists nowhere else in git.
