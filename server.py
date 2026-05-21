"""HTTP wrapper for the auth Lambda handler (Fase 3 — Kind / Traefik gateway)."""

from __future__ import annotations

import json
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.handler import handler

LOG = logging.getLogger("auth-lambda-http")
app = FastAPI(title="Oficina Auth CPF", version="1.0.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "UP"}


@app.post("/token")
async def token(request: Request) -> JSONResponse:
    body = (await request.body()).decode("utf-8") or "{}"
    event = {"body": body}
    result = handler(event, None)
    try:
        payload = json.loads(result.get("body") or "{}")
    except json.JSONDecodeError:
        payload = {"error": "Resposta invalida"}
    return JSONResponse(content=payload, status_code=int(result.get("statusCode", 500)))
