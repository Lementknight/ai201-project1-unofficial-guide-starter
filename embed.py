#!/usr/bin/env python3
"""
Milestone 4: Embedding & Vector Store
Loads chunks from documents/, embeds with all-mpnet-base-v2, stores in ChromaDB.
"""

import json
import os
from pathlib import Path
from typing import Optional

import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "benefits_guide"
EMBED_MODEL = "all-mpnet-base-v2"
DOCUMENTS_DIR = "documents"


def load_chunks(documents_dir: str = DOCUMENTS_DIR) -> list[dict]:
    """
    Load all *.json files from documents_dir.
    Returns list of dicts with keys: source_url, chunk_index, chunk_text, char_count.
    Raises FileNotFoundError if no JSON files found.
    """
    doc_path = Path(documents_dir)
    if not doc_path.exists():
        raise FileNotFoundError(f"Directory {documents_dir} not found. Run ingest.py first.")

    chunks = []
    for json_file in sorted(doc_path.glob("chunk_*.json")):
        with open(json_file, "r") as f:
            chunks.append(json.load(f))

    if not chunks:
        raise FileNotFoundError(f"No chunk_*.json files found in {documents_dir}. Run ingest.py first.")

    print(f"Loaded {len(chunks)} chunks from {documents_dir}")
    return chunks


def build_collection(
    chunks: list[dict],
    model_name: str = EMBED_MODEL,
    chroma_dir: str = CHROMA_DIR,
    collection_name: str = COLLECTION_NAME,
) -> chromadb.Collection:
    """
    Initialize embedding model and ChromaDB collection.
    If collection already has the correct number of documents, returns early (idempotent).
    Otherwise, embeds all chunks and upserts to ChromaDB.
    """
    print(f"\nInitializing embedding model: {model_name}")
    model = SentenceTransformer(model_name)

    print(f"Initializing ChromaDB (persisted to {chroma_dir})")
    client = chromadb.PersistentClient(path=chroma_dir)

    collection = client.get_or_create_collection(name=collection_name)

    # Idempotency check: if collection already has all chunks, skip re-embedding
    if collection.count() == len(chunks):
        print(f"Collection already has {len(chunks)} documents. Skipping re-embedding.")
        return collection

    print(f"Encoding {len(chunks)} chunks...")
    chunk_texts = [c["chunk_text"] for c in chunks]
    embeddings = model.encode(chunk_texts, show_progress_bar=True).tolist()

    print(f"Upserting to ChromaDB collection '{collection_name}'...")
    collection.upsert(
        ids=[str(c["chunk_index"]) for c in chunks],
        embeddings=embeddings,
        documents=chunk_texts,
        metadatas=[
            {"source_url": c["source_url"], "chunk_index": c["chunk_index"]}
            for c in chunks
        ],
    )

    print(f"✓ Collection now has {collection.count()} documents")
    return collection


def retrieve(
    query: str,
    top_k: int = 3,
    collection_name: str = COLLECTION_NAME,
    chroma_dir: str = CHROMA_DIR,
    model_name: str = EMBED_MODEL,
) -> list[dict]:
    """
    Retrieve top-k chunks most similar to query.
    Returns list of dicts with keys: chunk_text, source_url, chunk_index, distance.
    """
    model = SentenceTransformer(model_name)
    client = chromadb.PersistentClient(path=chroma_dir)
    collection = client.get_or_create_collection(name=collection_name)

    # Embed query
    query_embedding = model.encode([query])[0].tolist()

    # Retrieve
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    # Unpack results into a list of dicts
    retrieved = []
    if results and results["documents"] and len(results["documents"]) > 0:
        for doc, metadata, distance in zip(
            results["documents"][0], results["metadatas"][0], results["distances"][0]
        ):
            retrieved.append(
                {
                    "chunk_text": doc,
                    "source_url": metadata["source_url"],
                    "chunk_index": metadata["chunk_index"],
                    "distance": distance,
                }
            )

    return retrieved


if __name__ == "__main__":
    try:
        chunks = load_chunks()
        collection = build_collection(chunks)
        print(f"\n✓ Embedding pipeline complete. Collection '{COLLECTION_NAME}' is ready.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
