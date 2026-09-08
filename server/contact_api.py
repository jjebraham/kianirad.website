"""Contact-form API for kianirad.website.

Secrets are read from environment variables; never commit them.
Run behind Nginx/Cloudflare and proxy /api/contact to this service.
"""

from __future__ import annotations

import asyncio
import os
import time
from collections import defaultdict, deque
from typing import Deque

import httpx
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator


BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
RATE_LIMIT = int(os.environ.get("CONTACT_RATE_LIMIT", "5"))
RATE_WINDOW_SECONDS = int(os.environ.get("CONTACT_RATE_WINDOW_SECONDS", "600"))

ALLOWED_ORIGINS = [
    "https://www.kianirad.website",
    "https://kianirad.website",
]

app = FastAPI(title="Kianirad Contact API", docs_url=None, redoc_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
    allow_credentials=False,
)

# Simple per-process limiter. This is sufficient for one small Uvicorn worker.
# If the service is later scaled to multiple workers/hosts, move rate state to Redis.
_hits: dict[str, Deque[float]] = defaultdict(deque)
_hits_lock = asyncio.Lock()


class ContactSubmission(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    contact: str = Field(min_length=2, max_length=200)
    need: str = Field(min_length=1, max_length=160)
    message: str = Field(min_length=5, max_length=5000)
    lang: str = Field(default="en", max_length=5)
    page: str = Field(default="", max_length=500)
    website: str = Field(default="", max_length=200)  # honeypot

    @field_validator("name", "contact", "need", "message", "lang", "page", "website")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()

    @field_validator("lang")
    @classmethod
    def supported_lang(cls, value: str) -> str:
        return value if value in {"en", "tr", "fa"} else "en"



def client_ip(request: Request) -> str:
    """Return the visitor address.

    Cloudflare's header is preferred because the origin is expected to sit behind
    Cloudflare. Keep the origin firewalled from arbitrary direct traffic so this
    header cannot be spoofed by bypassing Cloudflare.
    """
    cf_ip = request.headers.get("CF-Connecting-IP", "").strip()
    if cf_ip:
        return cf_ip[:80]
    if request.client:
        return request.client.host[:80]
    return "unknown"


async def enforce_rate_limit(ip: str) -> None:
    now = time.monotonic()
    cutoff = now - RATE_WINDOW_SECONDS
    async with _hits_lock:
        q = _hits[ip]
        while q and q[0] < cutoff:
            q.popleft()
        if len(q) >= RATE_LIMIT:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many submissions",
            )
        q.append(now)



def telegram_text(data: ContactSubmission, ip: str) -> str:
    # Plain text on purpose: user input is never interpreted as Telegram HTML/Markdown.
    return (
        "New kianirad.website enquiry\n\n"
        f"Name: {data.name}\n"
        f"Contact: {data.contact}\n"
        f"Need: {data.need}\n"
        f"Language: {data.lang}\n"
        f"Page: {data.page or '-'}\n"
        f"IP: {ip}\n\n"
        f"{data.message}"
    )


@app.get("/health")
async def health() -> dict[str, bool]:
    return {"ok": True}


@app.post("/contact")
async def submit_contact(data: ContactSubmission, request: Request) -> dict[str, bool]:
    # Filled honeypots look successful to bots but are intentionally discarded.
    if data.website:
        return {"ok": True}

    ip = client_ip(request)
    await enforce_rate_limit(ip)

    if not BOT_TOKEN or not CHAT_ID:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Contact service is not configured",
        )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": telegram_text(data, ip)}

    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Message delivery failed",
        ) from exc

    return {"ok": True}
