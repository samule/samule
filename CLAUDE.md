# samule/samule (GitHub profile README)

This repo is Santiago's GitHub profile page: `README.md` renders on github.com/samule.

- The card on top is two generated SVGs (`assets/card-dark.svg`, `assets/card-light.svg`), swapped by a `<picture>` tag for GitHub's dark/light theme. Don't hand-edit the SVGs.
- To change the text on the card: edit `INFO` in `scripts/make_card.py`, then `python3 scripts/make_card.py` (stdlib only).
- To regenerate the portrait you need the source photo (`DSC_0248.png`, attached to the "GitHub profile intro page" task in Notion; it is not committed). Then:
  `python3 scripts/make_ascii.py PHOTO > assets/portrait-dark.txt` and `python3 scripts/make_ascii.py PHOTO --light > assets/portrait-light.txt`, then `python3 scripts/make_card.py`. Needs Pillow + numpy. The head silhouette polygon in that script is hand-traced for that exact photo; a different photo needs a new polygon.
- The portrait is dithered onto a short ramp (` .:+*#@`) on purpose: Santiago found long ramps (every cell a mid-weight char) fuzzy and wanted empty space between characters. Keep the ramp short.
- The portrait uses a smaller font than the info text (`AFONT`/`ALINE` vs `FONT`/`LINE` in `make_card.py`) so 84 columns fit next to the info column.
- Keep each right-hand value short: a row is 60 characters wide (`WIDTH`), so key + value must fit in about 55.
- Only link public repos in the README; private projects are mentioned without links.
