# ⭐️ Pro Plan API
A simple REST API for managing Pro plan subscriptions.

## ⚡ Highlights
- **Minimalist domain design**
- **Ready to run** — out of the box with Docker
- **Unit and functional tests** — covering domain logic and API behavior

## 📦 Subscription
- **Single subscription model**
- **Identified by email** — no external identifiers required
- **Simple management** — no states, just an active flag

## 🔌 API Endpoints
- **Health check** — service availability
- **Create or get subscription** — returns the subscription ID
- **Get subscription** — retrieves the full subscription

## 🏗️ Stack & Architecture
- **Python + FastAPI**
- **Clean Architecture**
- **Use-case driven design**
- **Rich domain models** — organized into domain modules
- **Value objects**
- **UUIDs** — primary identifiers

## ⚙️ Getting Started
### Requirements
- Docker
- Docker Compose

### Development
Run the project:
```shell
docker compose up -d
```
This starts the whole project, including database migrations, which run automatically before the API starts.

#### URLs
API Base URL: http://localhost/api

##### Tools
- API Docs: http://localhost/docs
- Mailcatcher: http://localhost:81

#### Commands
Useful commands are available in the [Makefile](./Makefile).

### Production
Run the project with the environment variables from [.env.dist](./.env.dist) set to production values. Also set `DATABASE_PASSWORD` for the `database` container to match the password in `DATABASE_URL`:
```shell
API_TOKEN='...' \
DATABASE_PASSWORD='...' \
DATABASE_URL='...' \
EMAIL_SENDER='...' \
SMTP_DSN='...' \
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 🎯 About the Project
An example project demonstrating backend system design.

## 🧑‍💼 Author
**Dušan Mlynarčík** — Senior Backend Engineer & App Builder

- LinkedIn: https://www.linkedin.com/in/dusanmlynarcik/
- GitHub: https://github.com/dusanmlynarcikdev
- Web: https://dusanmlynarcik.com
