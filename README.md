# Sistema de Consulta de Placas — Roubo/Furto

API REST desenvolvida com **FastAPI** para consulta de veículos com restrição de roubo ou furto.

---

## Tecnologias

- Python 3.11 + FastAPI
- SQLAlchemy 2 (async) + PostgreSQL
- Autenticação JWT (python-jose + passlib/bcrypt)
- Pytest + httpx para testes
- Docker + Docker Compose

---

## Configuração do ambiente

### 1. Clone e instale as dependências

```bash
git clone <seu-repo>
cd backendv2
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure o `.env`

Copie o `.env.example` e ajuste os valores:

```bash
cp .env.example .env
```

> ⚠️ Nunca suba o `.env` real para o repositório. Ele já está no `.gitignore`.

Variáveis obrigatórias:

| Variável | Descrição |
|---|---|
| `DB_USER` | Usuário do PostgreSQL |
| `DB_PASSWORD` | Senha do PostgreSQL |
| `DB_HOST` | Host do banco |
| `DB_PORT` | Porta (padrão: 5432) |
| `DB_NAME` | Nome do banco |
| `SECRET_KEY` | Chave secreta para JWT (use uma chave forte em produção) |
| `ALGORITHM` | Algoritmo JWT (padrão: HS256) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiração do token em minutos |

### 3. Crie as tabelas

```bash
python criar_tabelas.py
```

### 4. Rode o servidor

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## Rodando com Docker

```bash
docker-compose up --build
```

O banco de dados e a API sobem juntos. A API aguarda o banco estar saudável antes de iniciar.

---

## Autenticação

A API usa **JWT Bearer Token**. Para obter um token:

```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=seu_login&password=sua_senha
```

Use o token retornado no header das requisições:

```http
Authorization: Bearer <token>
```

### Níveis de acesso

| Tipo | Permissões |
|---|---|
| `admin` | Acesso total (criar, editar, deletar, listar tudo) |
| `operador` | Consultar placas, ver listas, ver próprio perfil |

---

## Endpoints principais

| Método | Rota | Descrição | Acesso |
|---|---|---|---|
| POST | `/api/v1/auth/login` | Login e geração de token | Público |
| POST | `/api/v1/usuarios/` | Criar usuário | Público |
| GET | `/api/v1/usuarios/me` | Meu perfil | Autenticado |
| GET | `/api/v1/veiculos/consultar/{placa}` | Consultar placa | Autenticado |
| POST | `/api/v1/veiculos/` | Cadastrar veículo | Admin |
| POST | `/api/v1/restricoes/` | Registrar restrição | Admin |

Documentação interativa completa disponível em: `http://localhost:8000/docs`

---

## Testes

```bash
pytest
```

Os testes usam banco SQLite em memória — não é necessário PostgreSQL rodando.

---

## Estrutura do projeto

```
backendv2/
├── api/
│   └── v1/
│       └── endpoints/      # Rotas da aplicação
├── core/
│   ├── configs.py          # Configurações e variáveis de ambiente
│   ├── database.py         # Engine e sessão do banco
│   ├── deps.py             # Dependências (auth, sessão)
│   └── security.py         # JWT e hash de senha
├── models/                 # Modelos SQLAlchemy
├── schemas/                # Schemas Pydantic
├── tests/                  # Testes automatizados
├── .env                    # Variáveis de ambiente (não versionar)
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
└── main.py
```
