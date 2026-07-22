# ⭐️ Pro Plan API
A simple REST API for managing Pro plan subscriptions.

## ⚡ Highlights
- **Minimalist domain design**
- **Ready to run** — out of the box with Docker
- **Unit and functional tests** — covering domain logic and API behavior

## 🙎‍♂️ Customers
- **One Pro plan per customer**
- **Identified by external ID** — a unique identifier provided by your app
- **Simple management** — no states, just an active Pro plan flag

> 💡 **Tip:** If you manage users for multiple apps at once, add a prefix to the customer external ID, e.g. `myapp:user-1`.

## 🔌 API Endpoints
- **Health check** — service availability
- **Stripe**
  - **Create checkout session**
  - **Handle webhooks** — `checkout.session.completed`, `customer.subscription.deleted`
  - **Create billing portal session**
- **Get customer** — retrieves customer details

> 💡 **Tip:** Use `success_url` parameter when creating a checkout session to perform additional post-payment actions, such as sending a Pro plan welcome email.

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
- API base URL: http://localhost:8081/api
- Swagger UI: http://localhost:8081/docs
- OpenAPI: http://localhost:8081/openapi.json

#### Commands
Useful commands are available in the [Makefile](./Makefile).

### Production
1) Download the production Docker Compose file:
```shell
curl -O https://raw.githubusercontent.com/dusanmlynarcikdev/pro-plan-api/main/docker-compose.prod.yml
```

2) Run the project with the environment variables from [.env.dist](./.env.dist) set to production values:
```shell
DATABASE_URL='...' \
STRIPE_API_KEY='...' \
STRIPE_PRICE_ID_MONTHLY='...' \
STRIPE_PRICE_ID_YEARLY='...' \
STRIPE_WEBHOOK_SECRET='...' \
docker compose -f docker-compose.prod.yml up -d
```

> 💡 **Tip:** The API container listens on port **8081** by default. To use a different port, set `API_PORT` environment variable when starting the container.

### API token

Access to the API requires an API token, which is sent as a Bearer token. 

An API token is generated automatically on the first application startup. Display it with:

```bash
docker compose logs api
```

The token is stored in the Docker volume, so it remains the same even after the container is restarted. 

To generate a new token, delete the existing token file and restart the container:

```bash
docker exec pro-plan-api rm /data/api-token
docker compose restart pro-plan-api
```

A new API token will be generated automatically during startup.

## 🎯 About the Project
An example project demonstrating backend system design.

## 🧑‍💻 Author
**Dušan Mlynarčík** — Senior Backend Engineer & App Builder

- LinkedIn: https://www.linkedin.com/in/dusanmlynarcik/
- GitHub: https://github.com/dusanmlynarcikdev
- Web: https://dusanmlynarcik.com
