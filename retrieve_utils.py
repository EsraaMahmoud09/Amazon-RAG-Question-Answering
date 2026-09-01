# ==========================================================
# Imports
# ==========================================================

import numpy as np
import pandas as pd
import chromadb

from sentence_transformers import SentenceTransformer, CrossEncoder
from rank_bm25 import BM25Okapi


# ==========================================================
# Load Models and Data
# ==========================================================

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="amazon_qa_semantic")

lexical_dataset = pd.read_csv("lexical_tokens.csv")
lexical_dataset["lexical_tokens"] = lexical_dataset["lexical_tokens"].apply(eval)

bm25 = BM25Okapi(lexical_dataset["lexical_tokens"].tolist())


# =============================================================================
# Semantic Retrieval
# =============================================================================
def semantic_search(query, top_k=5):

    query_embedding = embedding_model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances"
        ],
    )

    return results


# =============================================================================
# BM25 Retrieval
# =============================================================================
def lexical_search(query, top_k=5):

    query_tokens = query.lower().split()
    scores = bm25.get_scores(query_tokens)
    top_indices = scores.argsort()[-top_k:][::-1]
    results = lexical_dataset.iloc[top_indices].copy()
    results["bm25_score"] = scores[top_indices]

    return results


# =============================================================================
# Hybrid Search
# =============================================================================
def hybrid_search(query, semantic_k=5, lexical_k=5):

    semantic_results = semantic_search(query, top_k=semantic_k)
    lexical_results = lexical_search(query, top_k=lexical_k)

    return {
        "semantic": semantic_results,
        "lexical": lexical_results,
    }


# =============================================================================
# CrossEncoder Reranking
# =============================================================================
def rerank_results(query, hybrid_results, top_k=5):
    """
    Re-rank retrieved documents using CrossEncoder.
    """

    candidates = []

    # ---------------- Semantic Results ----------------
    semantic_docs = hybrid_results["semantic"]["documents"][0]
    semantic_meta = hybrid_results["semantic"]["metadatas"][0]

    for doc, meta in zip(semantic_docs, semantic_meta):
        candidates.append({
            "document": doc,
            "metadata": meta,
            "source": "semantic"
        })

    # ---------------- Lexical Results ----------------
    for _, row in hybrid_results["lexical"].iterrows():
        candidates.append({
            "document": row["chunk_text"],
            "metadata": {
                "QuestionID": row["QuestionID"],
                "Category": row["Category"],
                "QuestionType": row["QuestionType"],
                "QuestionTime": row["QuestionTime"]
            },
            "source": "lexical"
        })

    # Create query-document pairs
    pairs = [(query, candidate["document"]) for candidate in candidates]

    # Predict relevance scores
    scores = reranker.predict(pairs)

    # Attach scores
    for candidate, score in zip(candidates, scores):
        candidate["rerank_score"] = float(score)

    # Sort by score
    candidates = sorted(
        candidates,
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return candidates[:top_k]


# =============================================================================
# Remove Duplicate Chunks
# =============================================================================
def remove_duplicates(reranked_results):
    """
    Remove duplicated chunks after reranking.
    """

    unique_chunks = []
    seen = set()

    for item in reranked_results:
        text = item["document"].strip()
        if text not in seen:
            seen.add(text)
            unique_chunks.append(item)

    return unique_chunks


# =============================================================================
# Context Building
# =============================================================================
def build_context(results, max_chunks=5):
    """
    Build the final context passed to the LLM containing clean review texts.
    """

    context = ""
    selected_chunks = results[:max_chunks]

    for i, item in enumerate(selected_chunks, start=1):
        text = item['document']
        
        # Clean question prefixes and keep only answer/review content
        if "Answer:" in text:
            text = text.split("Answer:")[-1].strip()
        elif "Question:" in text:
            text = text.split("?")[-1].replace("Answer:", "").strip()

        context += f"Review {i}:\n{text}\n\n"

    return context


# =============================================================================
# Retrieve Final Context
# =============================================================================
def retrieve_context(query):

    # -------------------------------
    # Hybrid Retrieval
    # -------------------------------
    hybrid_results = hybrid_search(query)

    # -------------------------------
    # CrossEncoder Reranking
    # -------------------------------
    reranked_results = rerank_results(query, hybrid_results, top_k=10)

    # -------------------------------
    # Remove Duplicate Chunks
    # -------------------------------
    unique_results = remove_duplicates(reranked_results)

    # -------------------------------
    # Build Context
    # -------------------------------
    final_context = build_context(unique_results, max_chunks=5)

    return final_context, unique_results
