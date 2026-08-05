# Pro Plan API

**An API that integrates with Stripe and handles paid plan subscriptions.**

## How It Works

```text
┌──────────────┐      ┌──────────────┐       ┌────────┐
│ Your Backend │ ───▶ │ Pro Plan API │ ◀───▶ │ Stripe │
└──────────────┘      └──────────────┘       └────────┘
```

## Main Highlights

✔️ **Fast and modern stack (Python, FastAPI)**  
✔️ **Simple to integrate and use**  
✔️ **Production-ready Docker image for amd64 and arm64**  
✔️ **Deployable in minutes**

## Why Use Pro Plan API?

- No need to integrate Stripe yourself
- Saves development time and effort
- Ensures a correct Stripe integration
- Allows teams to focus on the core product
- Helps ship products faster

## Features

- Creates Stripe Checkout and Billing Portal sessions
- Synchronizes subscription access via Stripe webhooks
- Supports trials, subscription pauses, and grace periods
- Returns subscription data for your UI
- Identifies customers by your own external IDs
- Does not store customer data

## Limitations

- Automatically synchronizes only subscriptions created through checkouts initiated via Pro Plan API
- Other subscriptions require manual setup for synchronization
- Supports only one subscription with a single price per customer
- Does not support more complex billing models, such as usage-based pricing
- Currently supports only PostgreSQL

---

## 🚀 Getting Started

To integrate Pro Plan API into your application, see the [Integration Guide](./.docs/integration-guide.md).

---

## 👤 Author

**Dušan Mlynarčík** — Senior Backend Engineer

- LinkedIn: https://www.linkedin.com/in/dusanmlynarcik/
- GitHub: https://github.com/dusanmlynarcikdev
- Web: https://dusanmlynarcik.com
