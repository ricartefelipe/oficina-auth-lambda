# Autenticacao CPF (funcao serverless) - Fase 3

Funcao **Python** que valida CPF, consulta o cliente no **RDS PostgreSQL** e emite **JWT** para a API Spring Boot.

## Comportamento (enunciado Fase 3)

1. Receber **CPF** via API Gateway HTTP.
2. Validar formato e digitos verificadores.
3. Consultar **clientes** (`clientes.cpf_cnpj`, `clientes.status`: ATIVO/INATIVO).
4. Emitir **JWT** HS256 com `issuer`, `sub`, `cliente_id`, `cliente_status`, `authorities: [ROLE_CLIENTE]`.

## Deploy AWS (producao de demonstracao)

**Deploy concretizado** em `sa-east-1` via Terraform no repositorio **oficina-app** (`infra/terraform/aws-auth-lambda/`):

| Recurso | Valor |
|---------|-------|
| Funcao Lambda | `oficina-auth-cpf-fn` |
| API Gateway (HTTP) | `https://i3te2gzkmk.execute-api.sa-east-1.amazonaws.com/token` |
| RDS | PostgreSQL gerenciado (repo **oficina-infra-database**) |
| Regiao | `sa-east-1` |

Teste:

```bash
curl -sS -X POST "https://i3te2gzkmk.execute-api.sa-east-1.amazonaws.com/token" \
  -H "Content-Type: application/json" \
  -d '{"cpf":"52998224725"}'
```

Codigo-fonte embarcado tambem em `oficina-app/auth-lambda/` (mesmo handler). Este repositorio mantem a funcao isolada para CI/CD e SAM.

### Alternativa: SAM

`template.yaml` + `sam build && sam deploy --guided` para deploy independente. A funcao deve ficar na **mesma VPC** do RDS; ajustar security groups.

## Variaveis

| Variavel | Descricao |
|----------|-----------|
| `JWT_SECRET` | Segredo partilhado com a app (minimo 32 caracteres) |
| `JWT_ISSUER` | Mesmo valor que `JWT_CPF_ISSUER` na app (`https://oficina.local/auth/cpf`) |
| `PGHOST` / credenciais | RDS PostgreSQL |

## Execucao local (teste)

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export JWT_SECRET=<segredo>
export JWT_ISSUER=https://oficina.local/auth/cpf
python -c "from src.handler import handler; print(handler({'body':'{\"cpf\":\"52998224725\"}'}, None))"
```
