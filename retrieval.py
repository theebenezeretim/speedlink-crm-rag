"""Hybrid retrieval over the current Markdown, with conversation-aware scoping.

The corpus is small, so score every section before selecting evidence. This
avoids FAISS's post-filter candidate limit and stale pickled document metadata.
"""
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
import math
import os
import re
from threading import RLock

from parse_kb import KB_PATH, parse_knowledge_base
from route_query import contains, detect_services, normalize, resolve_services, workspace_types

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
STOP_WORDS = set("a an the is are do does i my me you your we our it its for to of in on and or with can want need please have how what which much about".split())


def tokens(text):
    return [word for word in normalize(text).split() if word not in STOP_WORDS]


@dataclass
class RetrievalResult:
    services: tuple
    documents: list
    rules: list
    mode: str
    warning: str | None = None
    needs_service: bool = False
    answer_corrected: bool = False

    @property
    def service(self):
        return ", ".join(self.services) if self.services else "general"


class Retriever:
    def __init__(self, documents, mode="hybrid"):
        if mode not in {"hybrid", "lexical"}:
            raise ValueError("RETRIEVAL_MODE must be hybrid or lexical.")
        self.documents = documents
        self.mode = mode
        self.warning = None
        self.embeddings = None
        self.vectors = None
        self._lock = RLock()
        self.counts = [Counter(tokens(doc.page_content)) for doc in documents]
        self.lengths = [sum(count.values()) for count in self.counts]
        self.average_length = sum(self.lengths) / len(self.lengths)
        frequency = Counter(word for count in self.counts for word in count)
        self.idf = {word: math.log(1 + (len(documents) - n + 0.5) / (n + 0.5))
                    for word, n in frequency.items()}

    def _semantic_scores(self, query):
        with self._lock:
            return self._semantic_scores_locked(query)

    def _semantic_scores_locked(self, query):
        if self.mode == "lexical":
            return [0.0] * len(self.documents)
        try:
            import numpy as np
            from langchain_huggingface import HuggingFaceEmbeddings
            if self.embeddings is None:
                offline = os.getenv("HF_HUB_OFFLINE", "").lower() in {"1", "true", "yes"}
                self.embeddings = HuggingFaceEmbeddings(
                    model_name=EMBEDDING_MODEL,
                    model_kwargs={"local_files_only": offline},
                    encode_kwargs={"normalize_embeddings": True},
                )
                self.vectors = np.asarray(self.embeddings.embed_documents(
                    [doc.page_content for doc in self.documents]), dtype="float32")
            vector = np.asarray(self.embeddings.embed_query(query), dtype="float32")
            return (self.vectors @ vector).tolist()
        except Exception as exc:
            # The demo remains usable, but degradation is visible to its operator.
            self.mode = "lexical"
            self.warning = f"Semantic search unavailable ({type(exc).__name__}); using keyword retrieval."
            return [0.0] * len(self.documents)

    def _lexical_scores(self, query):
        scores = []
        for counts, length in zip(self.counts, self.lengths):
            score = 0.0
            for word in set(tokens(query)):
                frequency = counts.get(word, 0)
                if frequency:
                    denominator = frequency + 1.5 * (0.25 + 0.75 * length / self.average_length)
                    score += self.idf.get(word, 0) * frequency * 2.5 / denominator
            scores.append(score)
        peak = max(scores, default=0) or 1.0
        return [score / peak for score in scores]

    def search(self, query, chat_history=(), k=8):
        if not query.strip():
            raise ValueError("Please enter a question.")
        if k < 1:
            raise ValueError("k must be at least 1.")
        services = resolve_services(query, chat_history)
        kinds = workspace_types(query)
        if "workspace" in services and not kinds:
            for message in reversed(list(chat_history)[-12:]):
                if message.get("role") != "user":
                    continue
                previous = message.get("content", "")
                previous_services = detect_services(previous)
                if previous_services and "workspace" not in previous_services:
                    break
                kinds = workspace_types(previous)
                if kinds:
                    break
        text = normalize(query)
        price = any(contains(text, term) for term in
                    ("price", "prices", "pricing", "cost", "fee", "fees", "how much", "rate", "rates", "plans", "charges"))
        amenities = any(contains(text, term) for term in
                        ("amenities", "facilities", "include", "included", "parking", "power", "seating", "capacity", "seats", "wifi", "internet", "equipment"))
        greeting = text in {"hi", "hello", "good morning", "good afternoon", "good evening"}
        overview = not services and contains(text, "services")
        needs_service = not services and (price or text in {"i want it", "how do i pay", "yes", "proceed", "what about that"})
        search_text = query + " " + " ".join(services) + " " + " ".join(kinds)
        if price:
            search_text += " pricing cost"
        if amenities and "workspace" in services:
            search_text += " amenities"
        lexical = self._lexical_scores(search_text)
        semantic = self._semantic_scores(search_text)
        topic_hints = []
        hint_phrases = {
            "course list": ("courses", "programs", "programmes", "offer", "available courses"),
            "registration": ("register", "registration", "how long", "requirements", "documents"),
            "coverage result": ("covered", "coverage", "outside", "not available"),
            "inquiry": ("installation", "location"),
            "no topic flow": ("no topic", "don t have a topic", "don t have a research topic", "choose a topic", "suggest topics"),
            "client with topic": ("my topic", "have a topic", "working prototype"),
            "deadline flow": ("deadline", "weeks", "finish", "timeline", "how long"),
            "confidentiality": ("confidential", "confidentiality", "nda", "intellectual property", "secure"),
            "postgraduate flow": ("phd", "msc", "postgraduate", "journal", "reviewer"),
            "payment flow": ("pay", "payment", "deposit", "upfront", "transfer"),
            "client expectation clarity": ("everything", "do it for me", "write it for me", "integrity"),
            "price objection": ("expensive", "too much"),
            "delay": ("need time", "think about"),
            "no money": ("no money", "don t have money", "cannot afford", "can t afford"),
            "not now": ("not now",),
            "closing": ("book", "proceed", "i want it", "invoice", "reserve"),
        }
        for topic, phrases in hint_phrases.items():
            if any(contains(text, phrase) for phrase in phrases):
                topic_hints.append(topic)
        if "training" in services and not price and any(contains(text, phrase) for phrase in
                ("learn", "i want cybersecurity", "i want web development", "i want data analytics", "enrol", "enroll")):
            topic_hints.append("qualification")
        if "research" in services and any(contains(text, phrase) for phrase in
                ("services", "what do you do", "what kind of support")):
            topic_hints.append("service explanation")
        ranked, rules = [], []
        for index, doc in enumerate(self.documents):
            meta = doc.metadata
            service, topic = meta["service"], meta["topic"]
            if meta["category"] == "global" or topic == "core rules":
                if topic == "core rules" and meta["service"] == "workspace" and "workspace" not in services:
                    continue
                if services and ((meta["domain"] == "research" and "research" in services)
                                 or (meta["domain"] == "commercial" and any(s != "research" for s in services))):
                    if meta["type"] == "BUSINESS_RULE":
                        rules.append(doc)
                continue
            if services and service not in services and service != "general":
                continue
            if services and service == "general" and topic not in topic_hints:
                continue
            if kinds and service == "workspace" and meta["service_type"] not in (*kinds, "general"):
                continue
            if price and service == "workspace" and not kinds:
                if meta["service_type"] != "general":
                    continue  # Identify a workspace before offering a room-specific price.
            if (greeting or needs_service) and not (meta["domain"] == "commercial" and meta["category"] == "general"):
                continue
            score = lexical[index] + 0.6 * max(0.0, semantic[index])
            if services and service in services:
                score += 0.35
            if price and meta["type"] == "PRICING":
                score += 1.5
            if kinds and meta["service_type"] in kinds:
                score += 0.8
            if amenities and "workspace" in services and topic == "amenities":
                score += 1.5
            if topic in topic_hints:
                score += 1.8
            if greeting and topic == "universal opening":
                score += 3
            if needs_service and topic == "service identification":
                score += 3
            if overview and topic == "service identification":
                score += 3
            if overview and topic in {"service context", "service explanation"}:
                score += 2.5
            if price and "workspace" in services and not kinds and topic == "pricing request handling":
                score += 3
            if not topic_hints and not price and not kinds and topic in {"entry", "inquiry", "universal opening"}:
                score += 0.5
            ranked.append((score, doc))
        ranked.sort(key=lambda pair: pair[0], reverse=True)
        chosen = []
        # Give each explicitly requested service a slot in comparison questions.
        if len(services) > 1:
            for service in services:
                match = next((doc for _, doc in ranked if doc.metadata["service"] == service), None)
                if match is not None:
                    chosen.append(match)
        for _, doc in ranked:
            if len(chosen) >= k:
                break
            if doc not in chosen:
                chosen.append(doc)
        return RetrievalResult(services, chosen[:k], rules, self.mode, self.warning, needs_service)


@lru_cache(maxsize=2)
def _cached_retriever(content, mode):
    return Retriever(parse_knowledge_base(content), mode)


def get_retriever(mode=None):
    # Cache by the content itself: a KB edit invalidates both documents and embeddings.
    return _cached_retriever(KB_PATH.read_text(encoding="utf-8"), mode or os.getenv("RETRIEVAL_MODE", "hybrid"))
