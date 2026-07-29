# ADR-003: Route AI requests through the Backoffice

## Status

Accepted

## Context

Users interact with the application through the Backoffice interface.

The Backoffice is responsible for rendering the user interface (SSR) and handling incoming HTTP requests. The AI Service should only process AI queries and should not be exposed directly to end users.

## Decision

When a user submits a question, the request is first sent to the Backoffice through the `/chat` endpoint.

The Backoffice forwards the query to the AI Service using its `/query` endpoint. The AI Service processes the request and, if needed, communicates with the Product MCP Server before returning the response.

```text
                 User
                   │
                   ▼
         Backoffice (SSR)
                   │
            POST /chat
                   │
                   ▼
            AI Service
            POST /query
                   │
                   ▼
         Inventory Agent
                   │
         (if tool required)
                   │
                   ▼
         Product MCP Server
                   │
                   ▼
             Product API
                   │
                   ▲
                   │
              AI Response
                   ▲
                   │
              Backoffice
                   ▲
                   │
                 User
```

## Consequences

Positive:

- The Backoffice remains the single entry point for users.
- The AI Service focuses only on AI processing.
- Authentication, authorization and request validation remain in the Backoffice.
- The AI Service can evolve independently from the user interface.

Trade-offs:

- AI requests require an additional HTTP request between the Backoffice and the AI Service.
- The Backoffice depends on the availability of the AI Service for AI-related features.