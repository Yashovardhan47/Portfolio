# K Yashovardhan — Engineering Portfolio

A data-driven Flask portfolio built to demonstrate the same engineering qualities it describes: clean separation of concerns, grounded retrieval, validated APIs, accessibility, automated tests and reproducible deployment.

## Highlights

- Recruiter-oriented case studies loaded from structured JSON
- Local retrieval-based portfolio assistant with explicit evidence links
- Validated, rate-limited Flask contact API with SQLite persistence
- Optional SMTP delivery without exposing browser credentials
- Responsive navigation, semantic markup and reduced-motion support
- Open Graph, structured data, robots and sitemap endpoints
- Security headers, health check, pytest suite and GitHub Actions CI
- Gunicorn and Render deployment configuration

The assistant does not invent experience or call a paid model. It ranks curated portfolio documents using token expansion and TF-IDF-style cosine similarity, then returns an answer with the relevant repository or certificate links.

## Structure

```text
Portfolio/
├── app.py
├── portfolio/
│   ├── __init__.py
│   ├── routes.py
│   └── services/
│       ├── assistant.py
│       └── contact.py
├── data/
│   ├── profile.json
│   └── projects.json
├── templates/index.html
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   └── profile assets
├── tests/test_app.py
└── .github/workflows/ci.yml
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env            # Windows: copy .env.example .env
flask --app app run --debug
```

Open <http://127.0.0.1:5000>.

## Verify

```bash
ruff check app.py portfolio tests
pytest -q
```

## Contact delivery

Every valid contact enquiry is persisted to the configured SQLite database. To also deliver it by email, set `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD` and `CONTACT_TO_EMAIL`. Never commit the real values.

## Production

Set a strong `SECRET_KEY`, the canonical `SITE_URL`, and durable `DATABASE_PATH`. The included `Procfile` and `render.yaml` run the app with Gunicorn and expose `/api/health` for health checks.

## Content updates

- Update personal information and skills in `data/profile.json`.
- Add or revise case studies in `data/projects.json`.
- Keep every claim evidence-based and link it to the relevant repository.
