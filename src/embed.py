"""
Embedding + Vector Store — Milestone 4, stage 1.

Loads the chunks produced by chunk.py, embeds each with all-MiniLM-L6-v2
(sentence-transformers, runs locally, no API key), and stores them in a
persistent ChromaDB collection together with source metadata for attribution.

Architecture (see planning.md):
    chunks.json  ->  all-MiniLM-L6-v2  ->  ChromaDB (cosine)  ->  retrieval

Design choices worth knowing:
  - We compute embeddings ourselves with SentenceTransformer and hand the
    vectors to Chroma (rather than letting Chroma pick a default model). This
    guarantees the SAME model embeds both the chunks here and the query in
    retrieve.py — mismatched models would silently wreck similarity scores.
  - normalize_embeddings=True + collection space "cosine" means Chroma returns
    a COSINE DISTANCE in [0, 2]: ~0 is near-identical, ~1 is unrelated. That's
    what lets us read a 0.18 as a strong match and a 0.65 as a weak one.

Run:   python src/embed.py
Store: chroma_db/   (persistent, gitignored)
"""

from __future__ import annotations

import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parent.parent
CHUNKS_FILE = ROOT / "chunks.json"
CHROMA_DIR = ROOT / "chroma_db"

MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "fire_chunks"

# Cached singletons so retrieve.py doesn't reload the model on every query.
_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    """Load all-MiniLM-L6-v2 once and reuse it."""
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def get_client() -> chromadb.api.ClientAPI:
    return chromadb.PersistentClient(path=str(CHROMA_DIR))


def get_collection(create: bool = False):
    """Return the chunks collection. With create=True, start it fresh.

    We use cosine space so distances are comparable across queries and map onto
    the 0.6-0.7 'weak match' thresholds in the evaluation rubric.
    """
    client = get_client()
    if create:
        # Drop any prior version so re-running doesn't duplicate or stack ids.
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:  # noqa: BLE001 - collection may not exist yet
            pass
        return client.create_collection(
            COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
        )
    return client.get_collection(COLLECTION_NAME)


def embed_texts(texts: list[str]):
    """Embed a list of strings into normalized 384-dim vectors."""
    return get_model().encode(
        texts,
        normalize_embeddings=True,    # unit vectors -> cosine distance behaves
        show_progress_bar=True,
        batch_size=64,
    ).tolist()


def main() -> None:
    chunks = json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))
    print(f"Loaded {len(chunks)} chunks from {CHUNKS_FILE.name}")

    collection = get_collection(create=True)

    ids = [c["id"] for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [
        {
            "source_file": c["source_file"],     # for attribution later
            "source_url": c["source_url"],
            "chunk_index": c["chunk_index"],      # position within its document
            "n_chars": c["n_chars"],
        }
        for c in chunks
    ]

    print(f"Embedding with {MODEL_NAME} ...")
    embeddings = embed_texts(documents)

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )

    count = collection.count()
    dim = len(embeddings[0]) if embeddings else 0
    print(f"\nStored {count} vectors ({dim}-dim) in collection "
          f"'{COLLECTION_NAME}' at {CHROMA_DIR}")
    if count != len(chunks):
        print(f"  WARNING: stored {count} but had {len(chunks)} chunks")


if __name__ == "__main__":
    main()
