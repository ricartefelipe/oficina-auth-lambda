# oficina-app
Aplicação principal **Spring Boot** da oficina (Tech Challenge Fase 3 — SOAT), executada em **Kubernetes**.
## Propósito
- APIs administrativas (JWT **Keycloak** / `ROLE_ADMIN`).
- APIs públicas (consulta de OS por `trackingCode`, aprovação de orçamento).
- APIs de cliente com JWT emitido pela **Lambda** (`ROLE_CLIENTE`), quando configurado.
- Ordem de serviço, catálogo, cadastros, métricas e notificações.
## Stack
- Java 21, Spring Boot 3.x
- PostgreSQL, Liquibase
- Docker / Kubernetes
- Observabilidade: Actuator, Prometheus (`/actuator/prometheus`), logs JSON (perfil `k8s`)
## Execução local
```bash
docker compose up --build
```
- Swagger: `http://localhost:8080/api/swagger-ui/index.html`
- Health: `http://localhost:8080/api/actuator/health`
## Deploy
- Imagem: `Dockerfile` + registry (ex.: GHCR).
- Cluster: aplicar manifests em `/k8s` (outro repo ou mesmo processo, conforme decisão da equipa).
- Variáveis: `DB_*`, `JWT_*`, `JWT_CPF_*` quando usar autenticação CPF.
## Diagrama (repositório)
```text
[API Gateway] ---> [Ingress K8s] ---> [Spring Boot]
                      /                    |
            [Lambda / JWT CPF]          [PostgreSQL]
```
## Documentação de API
- **Swagger / OpenAPI:** `/api/swagger-ui` (com `context-path` `/api`).
## Convite
Adicionar **`soat-architecture`** com leitura (portal SOAT).