# ⭐️ Pro Plan API

A simple REST API for managing Pro plan subscriptions.

> 🚧 Work in progress — actively being developed

## ⚡ Highlights
- **Minimalist domain design**
- **Authentication-free** — intended for backend services
- **Ready to run** — out of the box with Docker
- **Unit and functional tests** — covering domain logic and API behavior

## 📦 Subscription
- **Single subscription model**
- **Identified by email** — no external identifiers required
- **Simple lifecycle management** — no states, only validity period
- **End-of-month renewals** — calendar-based, including leap years

## 🏗️ Stack & Architecture
- **Python + FastAPI**
- **Clean Architecture**
- **Use-case driven design**
- **Rich domain models** — organized into domain modules
- **Value Objects & UUIDs** — primary identifiers

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