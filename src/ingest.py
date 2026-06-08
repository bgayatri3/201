"""
Document Ingestion — Milestone 3, stage 1.

Scrapes the 10 FIRE sources listed in planning.md, extracts the substantive
content, cleans away boilerplate (nav, cookie banners, footers, share buttons,
HTML entities), and writes one cleaned .txt file per source.

Extraction paths (per source):
  1. Local override -> if documents/manual/<slug>.{html,htm,txt,md} exists, ingest
     that instead of hitting the network. Used for the 4 sources whose anti-bot
     systems block scripted scraping (both Reddit URLs, Bogleheads, US News):
     save the page from a browser into documents/manual/ and it's picked up here.
  2. Reddit URLs    -> the public .json endpoint (when reachable).
  3. Everything else -> requests + BeautifulSoup main-content extraction.

Run:  python src/ingest.py
Output: documents/<slug>.txt   (cleaned, ready for chunking)
"""

from __future__ import annotations

import hashlib
import html
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Sources (mirrors the Documents table in planning.md)
# ---------------------------------------------------------------------------
SOURCES = [
    ("vanguard_early_retirement_4pct",
     "https://investor.vanguard.com/investor-resources-education/retirement/early-retirement"),
    ("investopedia_fire_explained",
     "https://www.investopedia.com/terms/f/financial-independence-retire-early-fire.asp"),
    ("reddit_financialindependence_faq",
     "https://www.reddit.com/r/financialindependence/wiki/faq/"),
    ("saxo_fire_guide",
     "https://www.home.saxo/learn/guides/trading-strategies/financial-independence-retire-early-fire-a-guide"),
    ("reddit_best_toughest_lessons",
     "https://www.reddit.com/r/financialindependence/comments/1nawcca/best_and_toughest_lessons_your_learned_on_your/"),
    ("bogleheads_three_fund_portfolio",
     "https://www.bogleheads.org/wiki/Three-fund_portfolio"),
    ("jlcollins_401k_403b_tsp_ira_roth_buckets",
     "https://jlcollinsnh.com/2015/06/02/stocks-part-viii-the-401k-403b-tsp-ira-roth-buckets/"),
    ("jlcollins_early_retirement_withdrawal_roth_ladder",
     "https://jlcollinsnh.com/2013/12/05/stocks-part-xx-early-retirement-withdrawal-strategies-and-roth-conversion-ladders-from-a-mad-fientist/"),
    ("usnews_7_lessons_fire",
     "https://money.usnews.com/money/retirement/aging/articles/lessons-from-those-who-retired-by-fire"),
    ("sofi_pros_cons_fire",
     "https://www.sofi.com/learn/content/pros-cons-of-fire-movement/"),
]

OUT_DIR = Path(__file__).resolve().parent.parent / "documents"
MANUAL_DIR = OUT_DIR / "manual"   # browser-saved pages for blocked sources

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Tags whose entire subtree is boilerplate and should be dropped before
# we pull text out of the page.
# Tags removed from the WHOLE document up front. These never hold article prose
# and would only add noise to content-root scoring.
GLOBAL_STRIP = ["script", "style", "noscript", "template"]

# Chrome tags stripped only from INSIDE the chosen content root — never before
# we pick the root. Investopedia's markup nests its <article> inside a <header>
# (article -> button -> header -> body) and ASP.NET wraps the body in a <form>,
# so stripping these globally up front wipes the real content. Pruning them only
# within the root we selected avoids that whole class of malformed-markup bugs.
INNER_STRIP = [
    "nav", "header", "footer", "aside", "svg", "iframe", "figure", "figcaption",
]

# CSS-ish substrings; an element is treated as chrome (cookie bars, ads,
# share/related widgets) only when its id/class contains one of these AND it
# is not an ancestor of the chosen content root — see extract_article.
JUNK_HINTS = [
    "cookie", "consent", "newsletter", "advert", "promo",
    "share-", "social-", "related", "recommend", "sidebar",
    "breadcrumb", "modal", "popup", "subscribe",
]


# ---------------------------------------------------------------------------
# Text cleaning shared by both extraction paths
# ---------------------------------------------------------------------------
def clean_text(text: str) -> str:
    """Decode HTML entities, drop boilerplate lines, normalize whitespace."""
    text = html.unescape(text)            # &amp; &#39; &nbsp; -> & ' (space)
    text = text.replace("\xa0", " ")      # stray non-breaking spaces
    text = text.replace("​", "")     # zero-width spaces

    # Strip any residual HTML tags that slipped through.
    text = re.sub(r"<[^>]+>", " ", text)

    line_junk = re.compile(
        r"^(read more|share|tweet|print|advertisement|sign up|subscribe|"
        r"related articles?|you might also like|menu|skip to (main )?content|"
        r"\d+ comments?|log ?in|sign ?in|cookie|table of contents)\b",
        re.IGNORECASE,
    )

    # Legal/marketing boilerplate that appears site-wide (esp. financial sites).
    boilerplate = re.compile(
        r"(investments? are not fdic insured|not bank guaranteed|may lose value|"
        r"member finra|sipc|for disclosures|fee schedule|terms of (use|service)|"
        r"privacy policy|all rights reserved|©|advisory services are provided|"
        r"sec-registered investment adviser)",
        re.IGNORECASE,
    )
    # Internal disclosure/tracking codes like "SOIN-Q325-004".
    disclosure_code = re.compile(r"^[A-Z]{2,}[-\dA-Z]{4,}$")

    cleaned_lines = []
    for raw in text.splitlines():
        line = re.sub(r"[ \t]+", " ", raw).strip()
        if not line:
            cleaned_lines.append("")          # keep paragraph breaks
            continue
        if line_junk.match(line) or boilerplate.search(line) or disclosure_code.match(line):
            continue
        # Drop one- or two-word nav fragments that are clearly not prose.
        if len(line) < 3:
            continue
        cleaned_lines.append(line)

    text = "\n".join(cleaned_lines)
    text = re.sub(r"\n{3,}", "\n\n", text)    # collapse big gaps
    return text.strip()


# ---------------------------------------------------------------------------
# Path A: generic article extraction
# ---------------------------------------------------------------------------
def extract_article(html_doc: str) -> str:
    soup = BeautifulSoup(html_doc, "lxml")

    # 1) Drop only script/style/noscript globally (no prose, just noise).
    for tag in soup(GLOBAL_STRIP):
        tag.decompose()

    def p_text_len(el) -> int:
        return sum(len(p.get_text(strip=True)) for p in el.find_all("p"))

    # 2) Pick the main-content container BEFORE stripping any chrome. Several
    #    candidates may exist (Saxo has an empty decorative <article> plus the
    #    real <main>), so score each by how much paragraph text it holds and keep
    #    the richest. Choosing the root first means malformed markup that nests
    #    the article inside a <header>/<form> can't cause us to delete it.
    candidates = (
        soup.find_all("article")
        + soup.find_all("main")
        + soup.find_all(attrs={"role": "main"})
    )
    root = max(candidates, key=p_text_len, default=None)
    if root is None or p_text_len(root) == 0:
        root = soup.body or soup

    # 3) Now strip chrome subtrees and junk widgets that live INSIDE the root.
    for tag in root.find_all(INNER_STRIP):
        tag.decompose()

    # 4) Remove junk widgets nested inside the root by id/class. Guard against
    #    tags already decomposed above (their .attrs becomes None -> error).
    for el in list(root.find_all(attrs={"class": True})) + list(root.find_all(attrs={"id": True})):
        if getattr(el, "decomposed", False) or el.attrs is None:
            continue
        cls = el.get("class") or []
        ident = (" ".join(cls) + " " + (el.get("id") or "")).lower()
        if any(hint in ident for hint in JUNK_HINTS):
            el.decompose()

    # 5) Pull text in document order, marking headings so the chunker can use
    #    them as natural paragraph boundaries. Skip link-only <li>/<p>: items
    #    whose text is mostly anchor text are related-article / "in this article"
    #    navigation widgets (e.g. Investopedia's link list, JL Collins' related
    #    posts), not prose.
    parts = []
    for el in root.find_all(["h1", "h2", "h3", "h4", "li", "p"]):
        text = el.get_text(" ", strip=True)
        if not text:
            continue
        if el.name.startswith("h"):
            parts.append(f"\n## {text}")
            continue
        anchors = el.find_all("a")
        if anchors:
            anchor_len = sum(len(a.get_text(strip=True)) for a in anchors)
            if anchor_len / max(len(text), 1) >= 0.7:
                continue   # navigation / related-links list item
        parts.append(text)

    return "\n\n".join(parts)


# ---------------------------------------------------------------------------
# Path B: Reddit via the public .json endpoint
# ---------------------------------------------------------------------------
def fetch_reddit(url: str) -> str:
    json_url = url.rstrip("/") + "/.json"
    resp = requests.get(json_url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    out: list[str] = []

    # Wiki pages: {"kind": "wikipage", "data": {"content_md": "..."}}
    if isinstance(data, dict) and data.get("kind") == "wikipage":
        out.append(data["data"].get("content_md", ""))
        return "\n\n".join(out)

    # Comment threads: [listing(post), listing(comments)]
    if isinstance(data, list):
        post = data[0]["data"]["children"][0]["data"]
        title = post.get("title", "")
        body = post.get("selftext", "")
        out.append(f"## {title}")
        if body:
            out.append(body)

        if len(data) > 1:
            for child in data[1]["data"]["children"]:
                if child.get("kind") != "t1":
                    continue
                comment = child["data"].get("body", "").strip()
                # Skip deleted/removed and trivial one-liners.
                if comment and comment not in ("[deleted]", "[removed]") and len(comment) > 40:
                    out.append(comment)

    return "\n\n".join(out)


def is_reddit(url: str) -> bool:
    return "reddit.com" in url


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
CACHE_DIR = OUT_DIR / ".cache_html"


def _cache_path(url: str) -> Path:
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]
    return CACHE_DIR / f"{digest}.html"


def fetch_html(url: str, retries: int = 3) -> str:
    """GET with on-disk caching and backed-off retries for 429/timeouts.

    Successful responses are cached so re-runs (to recover a failed source)
    don't re-hammer the sites that already worked.
    """
    cached = _cache_path(url)
    if cached.exists():
        return cached.read_text(encoding="utf-8")

    last = None
    for attempt in range(retries + 1):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=45)
            if resp.status_code == 429:
                raise requests.HTTPError("429 Too Many Requests")
            resp.raise_for_status()
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            cached.write_text(resp.text, encoding="utf-8")
            return resp.text
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(5 * (attempt + 1))  # 5s, 10s, 15s backoff (esp. for 429)
    raise last


def find_manual_file(slug: str) -> Path | None:
    """Return a browser-saved file for this slug, if the user provided one."""
    for ext in (".html", ".htm", ".txt", ".md"):
        candidate = MANUAL_DIR / f"{slug}{ext}"
        if candidate.exists():
            return candidate
    return None


def ingest_one(slug: str, url: str) -> tuple[str, int, str]:
    manual = find_manual_file(slug)
    if manual is not None:
        text = manual.read_text(encoding="utf-8", errors="ignore")
        # If the saved file already carries a SOURCE:/TITLE: header (e.g. copied
        # from our own output format), drop it so we don't double the header.
        text = re.sub(r"\A\s*SOURCE:.*\n(TITLE:.*\n)?", "", text)
        # HTML saves go through the extractor; .txt/.md are already plain text.
        raw = extract_article(text) if manual.suffix in (".html", ".htm") else text
        origin = f"local:{manual.name}"
    elif is_reddit(url):
        raw = fetch_reddit(url)
        origin = "scraped"
    else:
        raw = extract_article(fetch_html(url))
        origin = "scraped"

    cleaned = clean_text(raw)
    # Prepend a source header so chunks downstream carry provenance.
    document = f"SOURCE: {url}\nTITLE: {slug}\n\n{cleaned}\n"

    out_path = OUT_DIR / f"{slug}.txt"
    out_path.write_text(document, encoding="utf-8")
    return out_path.name, len(cleaned), origin


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Writing cleaned documents to {OUT_DIR}\n")

    for slug, url in SOURCES:
        try:
            name, n_chars, origin = ingest_one(slug, url)
            flag = "  <-- LOW, check manually" if n_chars < 500 else ""
            print(f"  OK   {name:<55} {n_chars:>7,} chars  [{origin}]{flag}")
        except Exception as exc:  # noqa: BLE001 - report and continue
            print(f"  FAIL {slug:<55} {type(exc).__name__}: {exc}")
            print(f"       -> blocked? save the page into "
                  f"documents/manual/{slug}.html (or .txt)")
        if find_manual_file(slug) is None and not _cache_path(url).exists():
            time.sleep(3)  # be polite only when we actually hit the network

    print("\nDone. Inspect a file before chunking, e.g.:")
    print("  python -c \"import pathlib,sys; "
          "print(pathlib.Path('documents/sofi_pros_cons_fire.txt').read_text(encoding='utf-8')[:2000])\"")


if __name__ == "__main__":
    main()
