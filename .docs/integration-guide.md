# Integration Guide

- [Prerequisites](#prerequisites)
- [Stripe API Key](#stripe-api-key)
- [Local Environment](#local-environment)
- [Authentication](#authentication)
- [Integration](#integration)
- [Stripe Events Destination](#stripe-events-destination)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

## Prerequisites

- Docker
- Docker Compose
- Stripe account

## Stripe API Key

Pro Plan API uses the Stripe API to create Stripe Checkout and Stripe Billing Portal sessions.
To authenticate these requests, provide your Stripe secret API key through the `STRIPE_API_KEY` environment variable.
The API key is available on the [API keys](https://dashboard.stripe.com/apikeys) page in the Stripe Dashboard.

## Local Environment

Run Pro Plan API locally to develop and test the integration with your application.

### 1) Clone the repository

```bash
git clone git@github.com:dusanmlynarcikdev/pro-plan-api.git
cd pro-plan-api
```

### 2) Create environment variables file

Create a `.env.local` file with Stripe environment variables based on `.env.dist`. You get the webhook secret in the next step, so you can leave it empty for now:

```text
STRIPE_API_KEY=...
STRIPE_WEBHOOK_SECRET=
```

### 3) Get the webhook secret

The local Docker setup includes a `stripe-cli` container. It forwards Stripe events to the Pro Plan API webhook endpoint and keeps subscriptions synchronized in the same way as in production.

Start the container:

```bash
docker compose --env-file .env.local up -d stripe-cli
```

It prints the webhook secret in its log:

```bash
docker logs pro-plan-api-stripe-cli-1
```

Copy the secret to `STRIPE_WEBHOOK_SECRET` in `.env.local`. The secret does not change, so you only need this once.

### 4) Run the rest of the project

```bash
docker compose --env-file .env.local up -d
```

or

```bash
make r
```

### URLs

- API base URL: http://localhost:8081/api (also serves as the health check endpoint)
- Swagger UI: http://localhost:8081/docs
- OpenAPI: http://localhost:8081/openapi.json

## Authentication

Access to Pro Plan API requires an API token, which is sent as a Bearer token.

```http
Authorization: Bearer <api-token>
```

### Retrieve the token

The API token is generated automatically on the first container start. Display it with:

```bash
docker exec pro-plan-api make at
```

The token is stored in a Docker volume, so it remains the same even after the container is restarted.

### Generate a new token

To generate a new token, delete the existing token and restart the container:

```bash
docker exec pro-plan-api rm /data/api-token
docker restart pro-plan-api
```

A new API token will be generated automatically during startup.

## Integration

The integration uses three endpoints. All of them require the API token described in [Authentication](#authentication).

### 1) Stripe Checkout

This endpoint starts the payment process for a customer. It also creates the customer in Pro Plan API when the customer does not exist yet. Pro Plan API then stores the subscription data for that customer.

**Endpoint:**

```http
POST /api/customers/stripe/checkout/sessions
```

**Example request:**

```json
{
  "customerExternalId": "019fd08e-56dd-7738-8310-57ec7e2eb921",
  "stripePriceId": "price-1",
  "successUrl": "https://yourdomain.com/success-payment",
  "trialDays": 7
}
```

- `customerExternalId` — your unique customer id
- `stripePriceId` — id of the Stripe price the customer subscribes to
- `successUrl` — where Stripe redirects the customer after payment
- `trialDays` — number of trial days, or `null` for no trial

> 💡 **Tip:** Use the `successUrl` to trigger additional post-payment actions, such as sending a paid plan welcome email.

**Example response:**

```json
{
  "url": "https://checkout.stripe.com/c/pay/cs_test_..."
}
```

- `url` — Stripe Checkout page to redirect the customer to

### 2) Customer subscription

This endpoint returns the customer's subscription data. Use it to decide whether to unlock paid features. It returns `404` when the customer does not exist in Pro Plan API.

**Endpoint:**

```http
GET /api/customers/{external_id}
```

**Example response:**

```json
{
  "stripe": {
    "canAccessBillingPortal": true,
    "subscription": {
      "isActive": true,
      "isTrial": true,
      "productId": "product-1",
      "currentPeriodEndAt": "2027-12-31T12:30:45Z",
      "cancelAt": null
    }
  }
}
```

- `canAccessBillingPortal` — `true` if the customer is linked to Stripe
- `subscription` — `null` until Stripe sends the first subscription event
- `isActive` — `true` if the customer has a paid plan
- `isTrial` — `true` if the customer is in a trial period
- `productId` — Stripe product id of the subscription, use it to identify the plan
- `currentPeriodEndAt` — end of the trial or a paid period
- `cancelAt` — a date if the subscription is going to be canceled

> ️️ℹ️ **Note:** All timestamps are in ISO 8601 format (UTC).

### 3) Stripe Billing Portal

> ℹ️ **Note:** Offer the portal only when `stripe.canAccessBillingPortal` is `true` in the customer response. Otherwise, the endpoint returns `409`.

This endpoint creates a Stripe Billing Portal session where the customer manages the subscription and billing details.

**Endpoint:**

```http
POST /api/customers/{external_id}/stripe/billing-portal/sessions
```

**Example response:**

```json
{
  "url": "https://billing.stripe.com/p/session/..."
}
```

- `url` — Stripe Billing Portal page to redirect the customer to

## Stripe Events Destination

> ℹ️ **Note:** This is not required for the local environment.

To synchronize subscriptions between Stripe and Pro Plan API, add an event destination on the [Webhooks](https://dashboard.stripe.com/webhooks) page in the Stripe Dashboard.

**Example endpoint URL:**

```text
https://yourdomain.com/api/webhooks/stripe
```

Select the following events:

- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`

Finally, copy the signing secret of the event destination and set the `STRIPE_WEBHOOK_SECRET` environment variable. Pro Plan API verifies every incoming event with this secret and rejects events that were not signed by Stripe.

> ️️ℹ️ **Note:** Pro Plan API processes the events as they arrive, so subscription changes are reflected almost immediately.

## Deployment

### 1) Download production files

Download the production Docker Compose file and the environment variables file template:

```bash
curl -o docker-compose.yml https://raw.githubusercontent.com/dusanmlynarcikdev/pro-plan-api/main/docker-compose.prod.yml \
     -o .env https://raw.githubusercontent.com/dusanmlynarcikdev/pro-plan-api/main/.env.dist
```

### 2) Set environment variables

Set the environment variables in the `.env` file to production values.

> 💡 **Tip:** Point `DATABASE_URL` to a database dedicated to Pro Plan API to avoid table name conflicts.

### 3) Run the project

```bash
docker compose up -d
```

> 💡 **Tip:** The API container listens on port **8081** by default. To use a different port, set the `API_PORT` environment variable when starting the container. This is also useful for zero-downtime deployment.

> 💡 **Tip:** The **latest** release is used by default. To pin a specific release, set the `API_VERSION` environment variable when starting the container.

**Example with custom port and API version:**

```bash
API_PORT=8080 API_VERSION=v1.2.0 docker compose up -d
```

### Health check

To verify that Pro Plan API is running, call the `/api` endpoint. It returns `204` on success and requires no authentication.

### Subsequent deployments

Before each subsequent deployment, update `docker-compose.yml` in case something has changed:

```bash
curl -o docker-compose.yml https://raw.githubusercontent.com/dusanmlynarcikdev/pro-plan-api/main/docker-compose.prod.yml
```

## Troubleshooting

Pro Plan API logs some events. The logs are written to the container output. If something goes wrong, check the logs first.

Display the logs with:

```bash
docker logs pro-plan-api
```

The logs contain:

- **Requests** — method, path, and response status code of every incoming request
- **Validation errors** — rejected requests together with the details of what was invalid
- **Stripe errors** — the reason a Stripe Checkout or Stripe Billing Portal session could not be created
- **Webhook errors** — errors that occurred during Stripe event processing

## Next Steps

🎉 Congratulations on successfully integrating Pro Plan API!

- Found a bug or need help? Open an issue on [GitHub Issues](https://github.com/dusanmlynarcikdev/pro-plan-api/issues).
- New versions are published on [GitHub Releases](https://github.com/dusanmlynarcikdev/pro-plan-api/releases).
