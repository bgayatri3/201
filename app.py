"""
Query Interface — Milestone 5.

A minimal Gradio web UI over the grounded-RAG pipeline. The answer and its
sources are shown in separate boxes so it's obvious the citations come from the
retrieval layer (programmatically), not from free-text the model wrote.

Run:  python app.py
Then open http://localhost:7860
"""

from __future__ import annotations

import sys
from pathlib import Path

# src/ holds the pipeline modules (query -> retrieve -> embed).
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import gradio as gr

from query import ask

DESCRIPTION = (
    "Ask a question about **FIRE** (Financial Independence, Retire Early). "
    "Answers are generated **only** from a curated set of 10 sources "
    "(Vanguard, Investopedia, JL Collins, Bogleheads, Reddit r/financialindependence, "
    "and more). If the sources don't cover your question, the assistant says so "
    "instead of guessing."
)

EXAMPLES = [
    "What is the difference between Lean FIRE and Fat FIRE?",
    "Why is diversification important when considering FIRE strategies?",
    "How is an FI number calculated?",
    "What are common investment recommendations in the FIRE community?",
    "What are the pros and cons of pursuing FIRE?",
]


def handle_query(question: str):
    question = (question or "").strip()
    if not question:
        return "Please enter a question.", ""
    try:
        result = ask(question)
    except Exception as exc:  # noqa: BLE001 - surface errors in the UI, don't crash
        return f"Error: {exc}", ""

    sources = result["sources"]
    sources_text = "\n".join(f"• {s}" for s in sources) if sources else \
        "(no sources — the answer was not found in the documents)"
    return result["answer"], sources_text


with gr.Blocks(title="The Unofficial FIRE Guide") as demo:
    gr.Markdown("# RAG on🔥: The Unofficial FIRE Guide")
    gr.Markdown(DESCRIPTION)

    with gr.Row():
        inp = gr.Textbox(
            label="Your question",
            placeholder="e.g. How is an FI number calculated?",
            lines=2,
            scale=4,
        )
        btn = gr.Button("Ask", variant="primary", scale=1)

    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from (sources)", lines=4)

    gr.Examples(examples=EXAMPLES, inputs=inp)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])


if __name__ == "__main__":
    demo.launch()
