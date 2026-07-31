# MVP Definition

## Overview

The MVP (Minimum Viable Product) provides a functional internal backoffice platform for managing business data and enabling AI-assisted queries.

The system is composed of several services running through Docker Compose:

* Backoffice service (Flask)
* MySQL database
* AI service
* MCP server

The goal of the MVP is to provide a stable foundation for managing resources, authenticating users, and integrating AI capabilities.

---

# Included Features

## Backoffice Service

The Backoffice service provides the main application API and business logic.

Included features:

* User management:

  * Create users
  * Retrieve users
  * Update users
  * Soft delete users

* Branch management:

  * Create branches
  * Retrieve branches
  * Update branches
  * Delete branches

* Stock management:

  * Create stock entries
  * Retrieve stock information
  * Update stock quantities
  * Manage product availability per branch

---

## Authentication

The MVP includes JWT-based authentication for backoffice users.

Included features:

* User login through `/auth/login`
* Password verification using Argon2 hashing
* JWT token generation
* Invalid credential handling
* Logout endpoint

Security requirements:

* Passwords are never stored in plaintext.
* Password hashes are never exposed through API responses.
* JWT secrets are stored using environment variables.

---

## AI Integration

The MVP includes AI-assisted queries.

Included features:

* Backoffice communication with the AI service
* AI request processing
* MCP tool integration when additional data is required
* Product-related information retrieval through available services

The AI service is integrated as an independent service and is not directly coupled to the Backoffice business logic.

---

## Infrastructure

The MVP includes:

* Docker Compose based development environment
* MySQL database container
* Environment variable configuration
* Separate services for Backoffice, AI processing and MCP communication

---

# Technical Architecture

The system follows a layered architecture:

```
HTTP Route
    |
    v
Service Layer
    |
    v
Repository Layer
    |
    v
Database
```

The Backoffice service communicates with external services through dedicated clients.

---

# Out of Scope

The following features are not included in the MVP:

* Advanced role and permission management
* Refresh token mechanism
* Token revocation system
* Full frontend application
* Production deployment
* Monitoring and observability system
* Automated CI/CD pipeline
* Advanced AI conversation memory

---

# Future Improvements

Possible future improvements include:

* Adding refresh tokens and token revocation
* Adding more granular authorization rules
* Improving AI capabilities
* Adding automated tests and coverage reporting
* Adding production deployment configuration

