# Manually-saved sources

Four of the ten sources block scripted scraping (Reddit blocks datacenter IPs
entirely; Bogleheads and US News use enterprise bot management). `ingest.py`
cannot fetch them, so save each page from your own browser into THIS folder.
The file name must match the slug exactly — the loader matches by name.

If a file below exists, `ingest.py` ingests it **instead of** scraping that URL,
runs it through the same cleaning pipeline, and writes `documents/<slug>.txt`.

| Save as (in this folder)                   | Source URL |
|--------------------------------------------|------------|
| `reddit_financialindependence_faq.txt`     | https://www.reddit.com/r/financialindependence/wiki/faq/ |
| `reddit_best_toughest_lessons.txt`         | https://www.reddit.com/r/financialindependence/comments/1nawcca/best_and_toughest_lessons_your_learned_on_your/ |
| `bogleheads_three_fund_portfolio.html`     | https://www.bogleheads.org/wiki/Three-fund_portfolio |
| `usnews_7_lessons_fire.html`               | https://money.usnews.com/money/retirement/aging/articles/lessons-from-those-who-retired-by-fire |

## How to save each one

**Reddit (two `.txt` files)** — the new Reddit UI renders comments with
JavaScript, so a raw HTML save is unreliable. Easiest path:
1. Open the URL in your browser.
2. Select the post + the comments you want (Ctrl+A works, or drag-select the
   thread body), copy, and paste into a plain-text file.
3. Save it here with the exact name above. The `.txt` path skips HTML parsing
   and just cleans the text, so pasted thread text comes through intact.
   *(Tip: `old.reddit.com/...` shows everything as plain text and is easy to
   copy. Keep the post title and the substantive comments; drop UI like
   "reply / share / report / X points".)*

**Bogleheads & US News (two `.html` files)** — these are clean article pages, so
let the extractor do the work:
1. Open the URL, press **Ctrl+S**, choose **"Webpage, HTML Only"**.
2. Save here with the exact name above. The loader runs `extract_article()` on
   it, picking the richest content container and stripping nav/ads.

## After saving

```
python src/ingest.py        # re-ingest; manual files override scraping
```
Each saved source should report `[local:<file>]` and a healthy character count.
Then inspect `documents/<slug>.txt` to confirm the content looks clean.
