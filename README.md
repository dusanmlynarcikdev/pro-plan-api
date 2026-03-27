# 💰 Pro Subscription Management API

A simple subscription management REST API for internal use — focused on a single subscription model.

> 🚧 Work in progress — actively being developed

## 🎯 Project Goals
- **FastAPI & Python:** Production-ready REST API built with a modern Python stack.
- **Clean Architecture:** Clear separation of concerns for long-term maintainability and scalability.
- **Real-World Domain:** A practical foundation you can use or extend.

## ⭐️ Highlights
- **Minimalist design**
- **Authentication-free** — intended for internal network environments
- **Ready to use** out of the box
- **Modern technology stack**

## 🧠 Domains

### Subscription
- **Single subscription model**
- **Identified by email**
- **One active subscription per email**
- **Full lifecycle management** (renewals, cancellations, expirations)
- **Payment required 7 days before period end**
- **7-day grace period** after a missed payment

### Payment
- **Extends the subscription** for the next billing period
- **Confirmation document** (proof of payment)
- **Payment history** with total paid amount per customer

## 🏗️ Stack & Architecture
- **Language:** Python + FastAPI
- **Architecture:** Clean Architecture (Domain, Application, Presentation, Infrastructure)
- **Patterns:** Use-case driven design (one command per use-case)
- **Domain:** Rich domain models (not anemic), organized into domain modules
- **Data:** Value Objects & UUIDs as primary identifies
- **Principles:** SOLID, KISS (Keep It Simple), DRY (Don't Repeat Yourself)
- **Quality:** Unit & functional tests covering domain logic and the entire API

## 💻 Dev Environment

### Requirements
- Docker
- Docker Compose

### Getting Started

Run the project:
```shell
docker compose up -d
```

The API will be available at:
- **API (base path & health check):** http://localhost
- **API Doc:** http://localhost/docs

## 👤 Maintainer

**Dušan Mlynarčík**  — Software Engineer & Product Builder

- LinkedIn: https://www.linkedin.com/in/dusanmlynarcik/
- GitHub: https://github.com/dusanmlynarcikdev
- Web: https://dusanmlynarcik.com