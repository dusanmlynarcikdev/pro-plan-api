# ⭐️ Pro Plan API

A simple REST API for managing Pro plan subscriptions.

> 🚧 Work in progress — actively being developed

## ⚡ Highlights
- **Minimalist design**
- **Authentication-free** — intended for backend services
- **Ready to use** — out of the box
- **Modern technology stack**

## 📦 Subscription
- **Single subscription model**
- **Identified by email** — no external identifiers for the client
- **Simple lifecycle management** — no states, only validity period
- **Grace period** — after a missed renewal, configurable

## 🏗️ Stack & Architecture
- **Python + FastAPI**
- **Clean Architecture**
- **Use-case driven design**
- **Rich domain models** — organized into domain modules
- **Value Objects & UUIDs** — primary identifiers
- **Unit & functional tests** — covering domain logic and the entire API

## ⚙️ Development

### Requirements
- Docker
- Docker Compose

### Getting Started

Run the project:
```shell
docker compose up -d
```

Run database migrations:
```shell
docker compose exec api make mu
```

The API will be available at:
- **API (base path & health check):** http://localhost
- **API Docs:** http://localhost/docs

## 👤 Author

**Dušan Mlynarčík** — Software Engineer & Product Builder

- LinkedIn: https://www.linkedin.com/in/dusanmlynarcik/
- GitHub: https://github.com/dusanmlynarcikdev
- Web: https://dusanmlynarcik.com