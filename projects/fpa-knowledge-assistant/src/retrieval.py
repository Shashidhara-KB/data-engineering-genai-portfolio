"""Small dependency-free retriever used to test RAG orchestration safely."""

import math
import re
from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class DocumentChunk:
    chunk_id: str
    source: str
    text: str


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def cosine_similarity(left: Counter, right: Counter) -> float:
    shared = set(left) & set(right)
    numerator = sum(left[token] * right[token] for token in shared)
    denominator = math.sqrt(sum(v * v for v in left.values())) * math.sqrt(
        sum(v * v for v in right.values())
    )
    return numerator / denominator if denominator else 0.0


def retrieve(query: str, chunks: list[DocumentChunk], top_k: int = 3) -> list[tuple[DocumentChunk, float]]:
    query_vector = Counter(tokenize(query))
    scored = [(chunk, cosine_similarity(query_vector, Counter(tokenize(chunk.text)))) for chunk in chunks]
    return sorted(scored, key=lambda item: item[1], reverse=True)[:top_k]


def build_grounded_context(results: list[tuple[DocumentChunk, float]], minimum_score: float = 0.1) -> str:
    accepted = [item for item in results if item[1] >= minimum_score]
    if not accepted:
        return "NO_RELEVANT_EVIDENCE"
    return "\n\n".join(
        f"[{chunk.chunk_id}] Source: {chunk.source}\n{chunk.text}" for chunk, _ in accepted
    )
