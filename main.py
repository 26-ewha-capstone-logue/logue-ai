import logging
import os
from urllib.error import URLError
from urllib.request import urlopen

from fastapi import FastAPI


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("logue_ai")

app = FastAPI(title="logue-ai", version="0.1.0")
UPSTREAM_HEALTH_URL = os.getenv("UPSTREAM_HEALTH_URL", "https://ai.logue-kr.site/health")
UPSTREAM_TIMEOUT_SEC = float(os.getenv("UPSTREAM_TIMEOUT_SEC", "3"))


def check_upstream_health(url: str, timeout_sec: float) -> tuple[bool, int | None, str | None]:
    try:
        with urlopen(url, timeout=timeout_sec) as response:
            status_code = int(response.status)
            return (200 <= status_code < 300, status_code, None)
    except URLError as exc:
        return (False, None, str(exc))
    except Exception as exc:  # pragma: no cover
        return (False, None, str(exc))


@app.get("/health")
def health() -> dict[str, object]:
    logger.info("Health check requested")
    upstream_ok, upstream_status_code, upstream_error = check_upstream_health(
        UPSTREAM_HEALTH_URL,
        UPSTREAM_TIMEOUT_SEC,
    )

    status = "ok" if upstream_ok else "degraded"
    if upstream_ok:
        logger.info("Upstream health check succeeded: %s", UPSTREAM_HEALTH_URL)
    else:
        logger.warning(
            "Upstream health check failed: %s status_code=%s error=%s",
            UPSTREAM_HEALTH_URL,
            upstream_status_code,
            upstream_error,
        )

    return {
        "status": status,
        "upstream": {
            "url": UPSTREAM_HEALTH_URL,
            "ok": upstream_ok,
            "status_code": upstream_status_code,
            "error": upstream_error,
        },
    }


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting development server")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
