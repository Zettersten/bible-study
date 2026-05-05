# Translations — Retrieval and Fallbacks

Default: **CSB** (Christian Standard Bible). The translation tag is per-run-overridable.

## CSB (default)

No public CSB API. Retrieve via `web_extract`:

```
https://www.biblegateway.com/passage/?search=<URL-encoded-ref>&version=CSB
```

Tips:

- The structured markdown summary `web_extract` returns is usually clean enough to lift into the study verbatim. Verify verse numbering before pasting.
- For multi-verse blocks, prefer a single `web_extract` call covering the whole range over many small calls.
- Bible.com's CSB endpoint (`https://www.bible.com/bible/1713/COL.2.CSB`) is mostly chrome around the text — Bible Gateway is the better source.
- Copyright: CSB is © 2017 Holman Bible Publishers. Quoting full chapters for personal study is fine; if the study ever moves to public distribution, audit usage.

## ESV (when explicitly requested)

The ESV API is the cleaner path. Token in `ESV_API_TOKEN` env var.

```
curl -H "Authorization: Token $ESV_API_TOKEN" \
  "https://api.esv.org/v3/passage/text/?q=<URL-encoded-ref>&include-headings=false&include-footnotes=false&include-verse-numbers=true"
```

Older studies in this repo use ESV (see `studies/2026-04-21-life-as-a-husband/`). Only switch to ESV when the user asks; otherwise stay with CSB.

## NASB / NKJV / others

If the user requests another translation, fall back to `web_extract` against Bible Gateway with the right `&version=` code:

| Translation | code |
|---|---|
| CSB | `CSB` |
| ESV | `ESV` |
| NASB1995 | `NASB1995` |
| NASB | `NASB` |
| NKJV | `NKJV` |
| NIV | `NIV` |
| KJV | `KJV` |

## Rate limiting and retries

- `web_extract` will sometimes refuse Bible Gateway under load. If that happens:
  1. Retry once with a slightly different URL (e.g. add `&interface=print`).
  2. Fall back to YouVersion's bible.com URL for the same passage.
  3. As a last resort, ask the user to paste the text — but only if the previous two failed *for the same passage twice*.
- Never invent verse text. If retrieval fails, surface the failure; do not paraphrase from memory.

## Translation tag rule

Whatever translation you used, every blockquote and full-verse citation must carry the same tag, in the same place: `**<Reference>** (<TRANS>)` immediately above the blockquote. Mixing translations inside one study is allowed *only* when comparing renderings — and even then, tag every quote.

## Always full-text rule

This is the rule that gets violated most often:

> Every verse referenced anywhere in either output file is printed in full.

That includes:
- Verses inside `Biblical Support` blocks (obviously).
- Verses cited in the answer prose ("see Romans 6:6").
- Verses in the `Cross-References` list at the bottom of `study.md`.
- Any verse named inside a word-study payload sentence.

If you find yourself writing `(see Rom 6:6)` without printing Rom 6:6 somewhere on the page, stop and add it.
