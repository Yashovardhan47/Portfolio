"""Small, auditable retrieval assistant grounded in portfolio data."""

from __future__ import annotations

import math
import re
from collections import Counter


TOKEN_RE = re.compile(r"[a-z0-9+#.-]+")
STOP_WORDS = {
    "a", "about", "an", "and", "are", "can", "do", "does", "for", "from",
    "has", "have", "he", "his", "how", "i", "in", "is", "me", "of", "on",
    "project", "projects", "show", "tell", "that", "the", "to", "was", "what",
    "which", "with", "yashovardhan", "yash",
}
ALIASES = {
    "api": {"fastapi", "flask", "rest"},
    "backend": {"python", "fastapi", "flask", "api"},
    "data": {"analytics", "pandas", "tableau", "science"},
    "finance": {"billing", "payment", "cash-flow", "safepay"},
    "fullstack": {"frontend", "backend", "react", "python", "database"},
    "ml": {"machine", "learning", "model", "yolov8"},
    "recruitment": {"hiring", "jobs", "recruiter", "candidate"},
}


def _tokens(text: str) -> list[str]:
    values = [token.strip(".-") for token in TOKEN_RE.findall(text.lower())]
    result = [token for token in values if token and token not in STOP_WORDS]
    expanded = list(result)
    for token in result:
        expanded.extend(ALIASES.get(token, set()))
    return expanded


def _documents(profile: dict, projects: list[dict]) -> list[dict]:
    documents = []
    for project in projects:
        text = " ".join(
            [
                project["title"],
                project["category"],
                project["tagline"],
                project["problem"],
                project["solution"],
                project["evidence"],
                " ".join(project["stack"]),
            ]
        )
        documents.append(
            {
                "kind": "project",
                "title": project["title"],
                "text": text,
                "url": project["github"],
                "project": project,
            }
        )
    documents.extend(
        [
            {
                "kind": "profile",
                "title": "Profile",
                "text": " ".join(
                    [profile["headline"], profile["summary"], " ".join(profile["roles"])]
                ),
                "url": profile["links"]["linkedin"],
            },
            {
                "kind": "skills",
                "title": "Skills",
                "text": " ".join(
                    item for group in profile["skills"] for item in group["items"]
                ),
                "url": profile["links"]["github"],
            },
            {
                "kind": "experience",
                "title": "Deloitte Data Analytics Simulation",
                "text": " ".join(profile["experience"]["highlights"]),
                "url": profile["experience"]["certificate"],
            },
        ]
    )
    return documents


def _rank(question: str, documents: list[dict]) -> list[tuple[float, dict]]:
    query = Counter(_tokens(question))
    document_tokens = [Counter(_tokens(item["text"])) for item in documents]
    count = len(documents)
    vocabulary = set(query)
    for tokens in document_tokens:
        vocabulary.update(tokens)
    frequencies = {
        word: sum(1 for tokens in document_tokens if tokens[word]) for word in vocabulary
    }

    def vector(counter: Counter) -> dict[str, float]:
        return {
            word: (1 + math.log(counter[word])) * math.log((count + 1) / (frequencies[word] + 1) + 1)
            for word in counter
            if counter[word]
        }

    query_vector = vector(query)
    ranked = []
    for item, tokens in zip(documents, document_tokens):
        document_vector = vector(tokens)
        dot = sum(query_vector.get(word, 0) * value for word, value in document_vector.items())
        q_norm = math.sqrt(sum(value * value for value in query_vector.values()))
        d_norm = math.sqrt(sum(value * value for value in document_vector.values()))
        score = dot / (q_norm * d_norm) if q_norm and d_norm else 0
        ranked.append((score, item))
    return sorted(ranked, key=lambda pair: pair[0], reverse=True)


def answer_question(question: str, profile: dict, projects: list[dict]) -> dict:
    """Return a concise answer plus explicit evidence links."""
    lowered = question.lower()
    documents = _documents(profile, projects)
    ranked = _rank(question, documents)
    sources: list[dict] = []

    if any(word in lowered for word in ("contact", "email", "reach", "hire him")):
        answer = (
            "Use the portfolio contact form or connect with Yashovardhan through LinkedIn. "
            "He is open to data, Python and full-stack opportunities."
        )
        sources = [{"label": "LinkedIn profile", "url": profile["links"]["linkedin"]}]
    elif any(word in lowered for word in ("resume", "cv")):
        answer = "Use the résumé button in the hero or About section to view the current PDF."
        sources = [{"label": "Résumé", "url": "/static/Yashovardhan_resume.pdf"}]
    elif any(word in lowered for word in ("strongest", "best", "flagship")):
        featured = [project for project in projects if project.get("featured")][:2]
        answer = (
            f"The strongest end-to-end engineering examples are {featured[0]['title']} and "
            f"{featured[1]['title']}. {featured[0]['title']} demonstrates "
            f"{featured[0]['evidence']} {featured[1]['title']} demonstrates "
            f"{featured[1]['evidence']}"
        )
        sources = [
            {"label": item["title"], "url": item["github"]} for item in featured
        ]
    elif any(word in lowered for word in ("experience", "deloitte", "internship")):
        answer = (
            "Yashovardhan completed Deloitte's Data Analytics Job Simulation, working with "
            "data preparation, Tableau dashboards and a pay-equality analysis. His portfolio "
            "also shows hands-on ownership through end-to-end projects."
        )
        sources = [
            {
                "label": "Deloitte completion certificate",
                "url": profile["experience"]["certificate"],
            }
        ]
    else:
        matches = [item for score, item in ranked if score > 0.04][:3]
        project_matches = [item for item in matches if item["kind"] == "project"]
        if project_matches:
            first = project_matches[0]["project"]
            answer = (
                f"The closest match is {first['title']}. {first['tagline']} "
                f"Evidence: {first['evidence']} "
                f"Stack: {', '.join(first['stack'][:6])}."
            )
            if len(project_matches) > 1:
                answer += " Also relevant: " + ", ".join(
                    item["title"] for item in project_matches[1:]
                ) + "."
            sources = [
                {"label": item["title"], "url": item["url"]} for item in project_matches
            ]
        elif any(item["kind"] == "skills" for item in matches):
            answer = (
                "His core stack spans Python, FastAPI, Flask, React, SQL/PostgreSQL, "
                "pandas, machine learning, Docker and GitHub-based delivery."
            )
            sources = [{"label": "GitHub profile", "url": profile["links"]["github"]}]
        else:
            answer = (
                "I can answer questions about Yashovardhan's projects, Python and data stack, "
                "experience, résumé, or how to contact him. Try asking which project uses FastAPI."
            )

    return {
        "answer": answer,
        "sources": sources,
        "grounded": True,
        "notice": "Generated only from this portfolio's verified project and profile data.",
    }
