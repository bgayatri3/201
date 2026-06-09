"""
Grounded Generation — Milestone 5.

End-to-end RAG answer function: retrieve -> build grounded prompt -> Groq LLM.

Grounding is enforced three ways, not merely suggested:
  1. A distance gate: chunks whose cosine distance exceeds RELEVANCE_CUTOFF are
     dropped. If none survive (the question is outside the corpus), we return the
     refusal string WITHOUT calling the LLM — so an off-topic question can't be
     answered from the model's training knowledge.
  2. A system prompt that restricts the model to the provided context and tells
     it to refuse with an exact sentence when the context is insufficient.
  3. Source attribution is assembled PROGRAMMATICALLY from the retrieved chunks'
     metadata (result["sources"]) — the LLM never invents which document an
     answer came from.

Public API:
    from query import ask
    result = ask("How is an FI number calculated?")
    # -> {"answer": str, "sources": [str, ...], "chunks": [dict, ...]}

Run as a script to test grounded generation end-to-end:
    python src/query.py
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from retrieve import TOP_K, retrieve

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

MODEL = "llama-3.3-70b-versatile"   # Groq free-tier, per planning.md
REFUSAL = "I don't have enough information on that."

# Cosine-distance ceiling for a chunk to count as relevant. In-domain queries
# in this corpus return best distances ~0.34-0.60; genuinely off-topic queries
# land well above this, so the gate cleanly refuses them. (See retrieve.py.)
RELEVANCE_CUTOFF = 0.80

SYSTEM_PROMPT = (
    "You are a factual assistant for questions about FIRE (Financial "
    "Independence, Retire Early). Answer the user's question using ONLY the "
    "information in the numbered context documents provided in the user "
    "message. Follow these rules strictly:\n"
    "1. Do NOT use any outside or prior knowledge. Every claim in your answer "
    "must be supported by the context.\n"
    "2. If the context does not contain enough information to answer, reply "
    f"with exactly: \"{REFUSAL}\" and nothing else.\n"
    "3. Do not invent facts, numbers, or sources.\n"
    "4. Be concise and directly answer the question."
)

_client: Groq | None = None


def get_client() -> Groq:
    global _client
    if _client is None:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key or api_key == "your_key_here":
            raise RuntimeError(
                "GROQ_API_KEY is not set. Copy .env.example to .env and add "
                "your free key from https://console.groq.com"
            )
        _client = Groq(api_key=api_key)
    return _client


def _format_context(chunks: list[dict]) -> str:
    """Number each chunk and label it with its source file for the model."""
    blocks = []
    for i, c in enumerate(chunks, 1):
        blocks.append(f"[{i}] (source: {c['source_file']})\n{c['text']}")
    return "\n\n".join(blocks)


def _unique_sources(chunks: list[dict]) -> list[str]:
    """Programmatic attribution: one entry per source file, best-ranked first."""
    seen: dict[str, str] = {}
    for c in chunks:                       # chunks already ordered by distance
        if c["source_file"] not in seen:
            seen[c["source_file"]] = c["source_url"]
    return [f"{name}  ({url})" if url else name for name, url in seen.items()]


def ask(question: str, k: int = TOP_K) -> dict:
    """Retrieve, then generate a grounded answer with programmatic citations."""
    hits = retrieve(question, k=k)
    relevant = [h for h in hits if h["distance"] <= RELEVANCE_CUTOFF]

    # Gate: nothing close enough -> refuse without involving the LLM at all.
    if not relevant:
        return {"answer": REFUSAL, "sources": [], "chunks": hits}

    context = _format_context(relevant)
    user_msg = (
        f"Context documents:\n\n{context}\n\n"
        f"Question: {question}\n\n"
        "Answer using only the context above."
    )

    completion = get_client().chat.completions.create(
        model=MODEL,
        temperature=0,                     # deterministic, minimizes drift
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
    )
    answer = completion.choices[0].message.content.strip()

    # If the model refused (context wasn't sufficient after all), don't attach
    # sources — the answer didn't come from them, so citing them would mislead.
    if answer.lower().startswith("i don't have enough information"):
        return {"answer": REFUSAL, "sources": [], "chunks": relevant}

    return {
        "answer": answer,
        "sources": _unique_sources(relevant),
        "chunks": relevant,
    }


# --- End-to-end grounding test ---------------------------------------------
TEST_QUERIES = [
    "What is the difference between Lean FIRE and Fat FIRE?",   # in-corpus
    "How is an FI number calculated?",                          # in-corpus
    "What are common investment recommendations in the FIRE community?",  # in-corpus
    "What is the best pizza topping in New York City?",         # OUT of corpus
]


def main() -> None:
    for q in TEST_QUERIES:
        print("=" * 78)
        print(f"Q: {q}")
        print("-" * 78)
        result = ask(q)
        print(result["answer"])
        if result["sources"]:
            print("\nRetrieved from:")
            for s in result["sources"]:
                print(f"  - {s}")
        else:
            print("\nRetrieved from: (none passed the relevance gate)")
        print()


if __name__ == "__main__":
    main()
