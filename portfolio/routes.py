"""Public pages and JSON APIs."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from flask import (
    Blueprint,
    Response,
    current_app,
    jsonify,
    render_template,
    request,
)

from .services.assistant import answer_question
from .services.contact import ContactError, accept_message


web = Blueprint("web", __name__)
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_json(name: str):
    return json.loads((DATA_DIR / name).read_text(encoding="utf-8"))


@web.get("/")
def home():
    profile = load_json("profile.json")
    projects = load_json("projects.json")
    return render_template(
        "index.html",
        profile=profile,
        projects=projects,
        site_url=current_app.config["SITE_URL"],
        current_year=datetime.now(timezone.utc).year,
    )


@web.get("/api/health")
def health():
    return jsonify(status="ok", service="portfolio")


@web.get("/api/projects")
def projects():
    return jsonify(projects=load_json("projects.json"))


@web.post("/api/assistant")
def assistant():
    payload = request.get_json(silent=True) or {}
    question = str(payload.get("question", "")).strip()
    if not 3 <= len(question) <= 400:
        return jsonify(error="Ask a question between 3 and 400 characters."), 400
    return jsonify(answer_question(question, load_json("profile.json"), load_json("projects.json")))


@web.post("/api/contact")
def contact():
    payload = request.get_json(silent=True) or {}
    try:
        result = accept_message(
            payload,
            database=current_app.config["DATABASE"],
            remote_addr=request.headers.get("X-Forwarded-For", request.remote_addr or "")
            .split(",")[0]
            .strip(),
        )
    except ContactError as exc:
        return jsonify(error=str(exc)), exc.status_code
    return jsonify(result), 201


@web.get("/robots.txt")
def robots():
    site_url = current_app.config["SITE_URL"]
    return Response(
        f"User-agent: *\nAllow: /\nSitemap: {site_url}/sitemap.xml\n",
        mimetype="text/plain",
    )


@web.get("/sitemap.xml")
def sitemap():
    site_url = current_app.config["SITE_URL"]
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"<url><loc>{site_url}/</loc><changefreq>monthly</changefreq>"
        "<priority>1.0</priority></url></urlset>"
    )
    return Response(xml, mimetype="application/xml")
