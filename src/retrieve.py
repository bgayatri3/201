"""
Retrieval — Milestone 4, stage 2.

A retrieval function that embeds a query with the SAME model used at index time
(all-MiniLM-L6-v2) and returns the top-k most similar chunks from ChromaDB,
each with its source metadata and cosine distance.

Run as a script to test retrieval against the planning.md evaluation queries:
    python src/retrieve.py

Or import and call:
    from retrieve import retrieve
    hits = retrieve("How is an FI number calculated?", k=5)
"""

from __future__ import annotations

import textwrap

from embed import get_collection, get_model

TOP_K = 5   # planning.md > Retrieval Approach


def retrieve(query: str, k: int = TOP_K) -> list[dict]:
    """Return the k chunks most similar to `query`, nearest first.

    Each result: {text, source_file, source_url, chunk_index, distance}.
    `distance` is cosine distance (0 = identical direction, higher = less
    related); see embed.py for why the collection uses cosine space.
    """
    model = get_model()
    collection = get_collection()

    query_vec = model.encode([query], normalize_embeddings=True).tolist()
    res = collection.query(
        query_embeddings=query_vec,
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    hits = []
    # Chroma nests results one level per query; we sent a single query -> [0].
    for doc, meta, dist in zip(
        res["documents"][0], res["metadatas"][0], res["distances"][0]
    ):
        hits.append({
            "text": doc,
            "source_file": meta["source_file"],
            "source_url": meta["source_url"],
            "chunk_index": meta["chunk_index"],
            "distance": dist,
        })
    return hits


# Evaluation queries from planning.md (using 4 of the 5; rubric asks for >=3).
EVAL_QUERIES = [
    "What is the difference between Lean FIRE and Fat FIRE?",
    "Why is diversification important when considering FIRE strategies?",
    "How is an FI number calculated?",
    "What are common investment recommendations in the FIRE community?",
]


def _print_hit(rank: int, hit: dict) -> None:
    flag = ""
    if hit["distance"] > 0.7:
        flag = "   <-- WEAK (>0.7)"
    elif hit["distance"] > 0.6:
        flag = "   <-- borderline (>0.6)"
    print(f"  [{rank}] distance={hit['distance']:.3f}  "
          f"source={hit['source_file']} (chunk {hit['chunk_index']}){flag}")
    snippet = textwrap.shorten(hit["text"].replace("\n", " "), width=320,
                               placeholder=" ...")
    print(f"      {snippet}")


def main() -> None:
    print(f"Testing retrieval (top-k={TOP_K}) against evaluation queries\n")
    for q in EVAL_QUERIES:
        print("=" * 78)
        print(f"QUERY: {q}")
        print("-" * 78)
        hits = retrieve(q, k=TOP_K)
        for i, hit in enumerate(hits, 1):
            _print_hit(i, hit)
        best = hits[0]["distance"] if hits else None
        if best is not None:
            verdict = ("strong" if best < 0.5 else
                       "ok" if best < 0.6 else "WEAK — investigate")
            print(f"\n  best distance: {best:.3f}  ->  {verdict}")
        print()


if __name__ == "__main__":
    main()
