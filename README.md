# Autenticacao CPF (funcao serverless) - Fase 3

Codigo destinado a viver num **repositorio proprio** (`oficina-auth-lambda`) com CI/CD. Mantido aqui como **fonte inicial** ate a divisao dos quatro repositorios.

## Comportamento alvo (enunciario Fase 3)

1. Receber **CPF** (API Gateway ou integracao direta).
2. Validar formato e digitos verificadores.
3. Consultar **clientes** na base PostgreSQL (`clientes.cpf_cnpj`, `clientes.status`: ATIVO/INATIVO).
4. Emitir **JWT** HS256 com `issuer`, `sub`, `cliente_id`, `cliente_status`, `authorities: [ROLE_CLIENTE]` consumivel pela aplicacao Spring (`security.cpf-jwt`). Resposta JSON inclui `cliente_id` e `cliente_status`.

## Variaveis

| Variavel | Descricao |
|----------|-----------|
| `JWT_SECRET` | Segredo partilhado com a app (minimo 32 caracteres recomendado) |
| `JWT_ISSUER` | Mesmo valor que `JWT_CPF_ISSUER` na app |
| `DATABASE_URL` | JDBC ou URI Postgres (ex.: RDS) |
| `DB_USER` / `DB_PASS` | Credenciais |

## Execucao local (teste)

```bash
cd auth-lambda
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
set JWT_SECRET=<JWT_SECRET>
set JWT_ISSUER=https://oficina.local/auth/cpf
python -c "from src.handler import handler; print(handler({'body':'{\"cpf\":\"00000000000\"}'}, None))"
```

## Deploy AWS

Usar **SAM** (`template.yaml`): `sam build && sam deploy --guided`.

A funcao deve ficar na **mesma VPC** do RDS ou usar **RDS Proxy**; ajustar security groups.
