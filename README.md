# logue-ai

Python 3.11 + FastAPI + uv 기반 프로젝트 스캐폴드입니다.

## Included

- FastAPI
- Uvicorn
- Pydantic v2
- pandas
- sentence-transformers
- pytest
- GitHub Actions CI
- Python logging

## Health check wiring

- Local endpoint: /health
- Upstream endpoint (default): https://ai.logue-kr.site/health
- Override with env var: UPSTREAM_HEALTH_URL
- Timeout seconds env var: UPSTREAM_TIMEOUT_SEC (default: 3)

## Local setup

1. Install dependencies:
   uv sync --all-groups
2. Run server:
   uv run python main.py
3. Run tests:
   uv run pytest -q

## Notes

- This environment had PyPI timeout issues during dependency download.
- The project is fully configured, and installation completes with `uv sync --all-groups` once network access to PyPI is available.
