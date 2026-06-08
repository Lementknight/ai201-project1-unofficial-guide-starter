#!/usr/bin/env python3
"""
Milestone 5: Grounded Generation & Gradio UI
Retrieves context, calls Groq LLM with grounding constraints, returns answer + sources.
"""

import os
from typing import Optional

import gradio as gr
from dotenv import load_dotenv
from groq import Groq

from embed import retrieve

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set in .env file")

SYSTEM_PROMPT = """You are a helpful assistant that explains employee benefits to recent college graduates preparing for their first job.

STRICT RULES FOR ANSWERING:
1. Answer ONLY using the information provided in the CONTEXT section below.
2. If the answer is not in the context, respond with: "I don't have enough information in my sources to answer that accurately. I recommend checking your company's HR portal or benefits handbook."
3. Do NOT use any prior knowledge about benefits, taxes, or finance that is not explicitly in the context.
4. After your answer, always list the sources you used in a "Sources:" section.
5. If multiple sources say different things, present both perspectives and cite each source explicitly.
6. Keep your answer clear, practical, and conversational — you are speaking to someone new to the workforce.
7. Avoid technical jargon; explain terms like HSA, HDHP, vesting cliff, etc. if they appear in your answer."""


def format_context(retrieved_chunks: list[dict]) -> str:
    """
    Format retrieved chunks into a numbered context block for the prompt.
    Each chunk is clearly labeled with its source URL.
    """
    if not retrieved_chunks:
        return "(No relevant information found)"

    context = "CONTEXT:\n"
    for i, chunk in enumerate(retrieved_chunks, 1):
        context += f"\n[{i}] SOURCE: {chunk['source_url']}\n"
        context += f"{chunk['chunk_text']}\n"
        context += "---"

    return context


def build_user_message(query: str, context: str) -> str:
    """
    Combine context and query into the user message for the LLM.
    """
    return f"""{context}

QUESTION: {query}

Please answer based only on the context above."""


def ask(query: str, top_k: int = 5) -> tuple[str, str]:
    """
    Full RAG pipeline call.
    Returns: (answer_text, sources_text)
    """
    # Retrieve
    retrieved_chunks = retrieve(query, top_k=top_k)

    # Format context
    context = format_context(retrieved_chunks)

    # Build message
    user_message = build_user_message(query, context)

    # Call Groq
    client = Groq(api_key=GROQ_API_KEY)

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=0.1,
            max_tokens=1024,
        )

        answer = response.choices[0].message.content

    except Exception as e:
        answer = f"Error calling Groq API: {e}"

    # Extract unique sources
    sources_set = {chunk["source_url"] for chunk in retrieved_chunks}
    sources_text = "\n".join(f"• {url}" for url in sorted(sources_set))

    return answer, sources_text


def gradio_ask(query: str) -> tuple[str, str]:
    """
    Wrapper for Gradio that returns answer and formatted sources.
    """
    if not query or len(query.strip()) < 5:
        return "Please ask a more specific question about employee benefits.", ""

    answer, sources = ask(query)
    return answer, sources


def build_interface():
    """
    Build and launch the Gradio web UI.
    """
    with gr.Blocks(title="Benefits Guide Q&A", css="""
        .header-section { margin-bottom: 1.5rem; }
        .query-section { margin-bottom: 1rem; }
        .results-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
        @media (max-width: 900px) { .results-row { grid-template-columns: 1fr; } }
        .footer-section { margin-top: 2rem; opacity: 0.85; }
    """) as interface:
        with gr.Group(elem_classes="header-section"):
            gr.Markdown("""
# Employee Benefits Guide — Q&A
Ask any question about employee benefits, 401(k)s, health insurance, vesting, negotiation, and more.
This system answers based on real guides for new grad hires.
            """)

        with gr.Group(elem_classes="query-section"):
            query_input = gr.Textbox(
                label="Your Question",
                placeholder="e.g., What is the difference between HDHP and PPO? What's the 401(k) match?",
                lines=4,
                interactive=True,
            )
            with gr.Row():
                submit_btn = gr.Button("Ask", variant="primary", size="lg", scale=1)
                gr.Markdown("**Tip:** Be specific for better answers!", scale=3)

        with gr.Row(elem_classes="results-row"):
            answer_output = gr.Textbox(
                label="Answer",
                interactive=False,
                lines=10,
            )
            sources_output = gr.Textbox(
                label="Sources Used",
                interactive=False,
                lines=10,
            )

        with gr.Group(elem_classes="footer-section"):
            gr.Markdown("""
**How this works:** Your question is embedded and matched against a database of benefits guides.
The top 5 most relevant sections are sent to an LLM (Groq Llama 70B) with strict instructions
to answer only from those sources, ensuring accuracy and transparency.
            """)

        submit_btn.click(
            fn=gradio_ask,
            inputs=[query_input],
            outputs=[answer_output, sources_output],
        )

        query_input.submit(
            fn=gradio_ask,
            inputs=[query_input],
            outputs=[answer_output, sources_output],
        )

    return interface


if __name__ == "__main__":
    print("Building Gradio interface...")
    interface = build_interface()
    print("Launching at http://127.0.0.1:7860")
    interface.launch()
