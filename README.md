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

- Removes the need to implement Stripe
- Saves development time and effort
- Ensures a correct Stripe integration
- Lets you focus on your core product
- Helps you ship your product faster

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

## 👤 Author

**Dušan Mlynarčík** — Senior Backend Engineer

- LinkedIn: https://www.linkedin.com/in/dusanmlynarcik/
- GitHub: https://github.com/dusanmlynarcikdev
- Web: https://dusanmlynarcik.com
