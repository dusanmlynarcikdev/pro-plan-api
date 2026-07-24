# Claude Instructions

## Application and Business Logic

Do not assume or infer application and business logic that is not explicitly stated. This includes HTTP status codes, error handling, validation rules, and edge-case behavior.

When the existing logic is ambiguous, or that may have multiple interpretations, ask how it is meant before planning or implementing a solution.

## Code Style and Design

Prefer simplicity to a robust solution. Follow existing patterns in the code but always consider the needs of the specific implementation.

When possible, prefer the latest stable versions of the language and libraries and all their available features that can make code more efficient. 

When caching is needed, cache only the smallest expensive unit and use an existing project pattern, such as @cache used by get_config. Account for the testing impact of caching

## Checks

Run all project checks (lint, types, tests, and database schema validation) inside the Docker `pro-plan-api` container.

Use the commands defined in the project [Makefile](./Makefile). For example:

```bash
docker exec pro-plan-api make cf
```

Do not run project tools directly on the host machine. 

There is no need to activate the project's virtual environment. All required dependencies, the Python environment, and the database are already available inside the `pro-plan-api` container.

## Third-Party Libraries and External Services

Never rely on memory when working with third-party libraries, frameworks, APIs, or external services and tools.

Always verify your assumptions against the official documentation. If the documentation is unclear, or does not fully answer the question, inspect the library's source code.

Do not guess or infer behavior. Only state something as a fact if you have verified it. Be confident only when the evidence supports it.
