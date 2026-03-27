import json
import os
import re
from datetime import datetime, timedelta, timezone

import jwt
import psycopg2


def _only_digits(s: str) -> str:
    return re.sub(r"\D", "", s or "")


def _cpf_valido(cpf: str) -> bool:
    d = _only_digits(cpf)
    if len(d) != 11 or len(set(d)) == 1:
        return False
    n = [int(x) for x in d]
    s1 = sum(n[i] * (10 - i) for i in range(9))
    r1 = s1 % 11
    dv1 = 0 if r1 < 2 else 11 - r1
    if dv1 != n[9]:
        return False
    s2 = sum(n[i] * (11 - i) for i in range(10))
    r2 = s2 % 11
    dv2 = 0 if r2 < 2 else 11 - r2
    return dv2 == n[10]


def _jwt_payload(cliente_id: str) -> dict:
    iss = os.environ.get("JWT_ISSUER", "https://oficina.local/auth/cpf")
    now = datetime.now(timezone.utc)
    return {
        "iss": iss,
        "sub": cliente_id,
        "cliente_id": cliente_id,
        "authorities": ["ROLE_CLIENTE"],
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=1)).timestamp()),
    }


def handler(event, context):
    secret = os.environ.get("JWT_SECRET", "")
    if not secret or len(secret) < 16:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "JWT_SECRET invalido"}),
        }

    body = {}
    if isinstance(event, dict):
        raw = event.get("body")
        if raw:
            body = json.loads(raw) if isinstance(raw, str) else raw
        elif event.get("cpf"):
            body = event

    cpf = _only_digits(body.get("cpf", ""))
    if not cpf or not _cpf_valido(cpf):
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "CPF invalido"}),
        }

    db_url = os.environ.get("DATABASE_URL", "")
    if not db_url:
        return {
            "statusCode": 503,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "DATABASE_URL nao configurado"}),
        }

    try:
        conn = psycopg2.connect(db_url)
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id::text, status FROM clientes WHERE cpf_cnpj = %s LIMIT 1",
                    (cpf,),
                )
                row = cur.fetchone()
        finally:
            conn.close()
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "database", "detail": str(e)}),
        }

    if not row:
        return {
            "statusCode": 404,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Cliente nao encontrado"}),
        }

    cliente_id = row[0]
    cliente_status = row[1] if len(row) > 1 else "ATIVO"
    payload = _jwt_payload(cliente_id)
    payload["cliente_status"] = cliente_status
    token = jwt.encode(payload, secret, algorithm="HS256")
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "access_token": token,
                "token_type": "Bearer",
                "expires_in": 3600,
                "cliente_id": cliente_id,
                "cliente_status": cliente_status,
            }
        ),
    }


if __name__ == "__main__":
    print(handler({"body": json.dumps({"cpf": "52998224725"})}, None))
