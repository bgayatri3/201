"""
Chunking — Milestone 3, stage 2.

Implements the Chunking Strategy from planning.md:
  - Paragraph-sized chunks, ~300-800 characters.
  - 10-20% overlap (~15%) to preserve concepts that span paragraph boundaries.
  - LangChain RecursiveCharacterTextSplitter, which respects natural boundaries
    (blank lines -> single newlines -> sentences -> words) instead of cutting
    mechanically mid-word.
  - Every chunk carries its source filename and URL for provenance.

Reads:  documents/*.txt   (cleaned output of ingest.py)
Writes: chunks.json       (list of {id, text, source_file, source_url, ...})

Run:  python src/chunk.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

DOCS_DIR = Path(__file__).resolve().parent.parent / "documents"
OUT_FILE = Path(__file__).resolve().parent.parent / "chunks.json"

# --- Chunking parameters (see planning.md > Chunking Strategy) --------------
CHUNK_SIZE = 800        # upper bound in characters; paragraph-sized
CHUNK_OVERLAP = 120     # ~15% overlap, within the planned 10-20% band
MIN_CHUNK = 200         # merge anything shorter so we don't emit fragments


def load_documents() -> list[dict]:
    """Read each cleaned .txt, splitting off the SOURCE/TITLE provenance header."""
    docs = []
    for path in sorted(DOCS_DIR.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        source_url = ""
        m = re.match(r"SOURCE:\s*(.*)\nTITLE:\s*(.*)\n", text)
        if m:
            source_url = m.group(1).strip()
            text = text[m.end():]          # drop the header from the body
        docs.append({
            "source_file": path.name,
            "source_url": source_url,
            "text": text.strip(),
        })
    return docs


def merge_short_chunks(chunks: list[str]) -> list[str]:
    """Fold sub-MIN_CHUNK pieces (lone headings, trailing scraps) into a neighbor.

    A standalone fragment like "## Pros of the FIRE Approach" carries no
    standalone meaning, so we attach it to an adjacent chunk instead of emitting
    it on its own. Short pieces merge forward (heading -> its section); a short
    tail with no following chunk merges backward.
    """
    merged: list[str] = []
    carry = ""
    for chunk in chunks:
        chunk = (carry + "\n\n" + chunk).strip() if carry else chunk
        carry = ""
        if len(chunk) < MIN_CHUNK:
            carry = chunk                 # hold it, prepend to the next chunk
        else:
            merged.append(chunk)
    if carry:                             # leftover tail: append to last chunk
        if merged:
            merged[-1] = (merged[-1] + "\n\n" + carry).strip()
        else:
            merged.append(carry)
    return merged


def chunk_text(text: str) -> list[str]:
    """Split one document into overlapping, paragraph-sized chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        # Prefer paragraph breaks, then lines, then sentences, then words.
        separators=["\n\n", "\n", ". ", "? ", "! ", " ", ""],
        length_function=len,
    )
    raw = [c.strip() for c in splitter.split_text(text) if c.strip()]
    return merge_short_chunks(raw)


def build_chunks() -> list[dict]:
    docs = load_documents()
    chunks: list[dict] = []
    for doc in docs:
        pieces = chunk_text(doc["text"])
        for i, piece in enumerate(pieces):
            chunks.append({
                "id": f"{doc['source_file']}::chunk_{i}",
                "text": piece,
                "source_file": doc["source_file"],
                "source_url": doc["source_url"],
                "chunk_index": i,
                "n_chars": len(piece),
            })
    return chunks, docs


def main() -> None:
    chunks, docs = build_chunks()
    OUT_FILE.write_text(json.dumps(chunks, indent=2, ensure_ascii=False), encoding="utf-8")

    sizes = [c["n_chars"] for c in chunks]
    print(f"Documents:     {len(docs)}")
    print(f"Total chunks:  {len(chunks)}")
    if sizes:
        print(f"Chunk size:    min={min(sizes)}  mean={sum(sizes)//len(sizes)}  max={max(sizes)} chars")
    print("Per document:")
    by_doc: dict[str, int] = {}
    for c in chunks:
        by_doc[c["source_file"]] = by_doc.get(c["source_file"], 0) + 1
    for name, n in by_doc.items():
        print(f"  {name:<55} {n:>3} chunks")
    print(f"\nWrote {OUT_FILE}")

    # Print 5 representative chunks (spread across the corpus) for inspection.
    print("\n" + "=" * 70)
    print("5 REPRESENTATIVE CHUNKS (read each: does it stand on its own?)")
    print("=" * 70)
    if chunks:
        step = max(1, len(chunks) // 5)
        for c in chunks[::step][:5]:
            print(f"\n--- {c['id']}  ({c['n_chars']} chars) ---")
            print(c["text"])


if __name__ == "__main__":
    main()
