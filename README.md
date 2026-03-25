# oficina-auth-lambda
Função **serverless** de autenticação do cliente por **CPF** (Tech Challenge Fase 3 — SOAT).
## Propósito
- Receber o CPF (via API Gateway ou integração).
- Validar dígitos verificadores.
- Consultar o cliente em **PostgreSQL** (`clientes.cpf_cnpj`, `clientes.status`).
- Devolver **JWT** HS256 (`ROLE_CLIENTE`) e metadados (`cliente_id`, `cliente_status`) consumíveis pela aplicação principal.
## Stack
- Python 3.12+
- `PyJWT`, `psycopg2`
- Deploy: **AWS SAM** (`template.yaml`) ou empacotamento para Lambda
## Execução local
```bash
cd auth-lambda
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
set JWT_SECRET=seu-segredo-minimo-32-chars-recomendado!!
set JWT_ISSUER=https://oficina.local/auth/cpf
set DATABASE_URL=postgresql://usuario:senha@host:5432/oficina
python -c "from src.handler import handler; print(handler({'body':'{\"cpf\":\"52998224725\"}'}, None))"
```
Variáveis: ver tabela no código-fonte (`README` interno ao pacote, se existir).
## Deploy
- `sam build && sam deploy --guided` (VPC/Security Group alinhados ao RDS).
- CI: GitHub Actions (lint/teste) no push/PR.
## Diagrama (repositório)
```text
[API Gateway] -> [Lambda auth] -> [RDS PostgreSQL]
                      |
                      v
                 JWT HS256
```
## Integração com a app
- A app Spring (`oficina-app`) valida o mesmo `issuer` e segredo (`security.cpf-jwt`).
## Documentação de API
Esta função é invocada pelo **Gateway** (não expõe Swagger próprio). Contrato do body: `{ "cpf": "00000000000" }`.
## Convite
Adicionar o utilizador **`soat-architecture`** com permissão de leitura (conforme portal SOAT).