# ADR-00X: Choice of JWT Authentication with PyJWT

## Status

Accepted

## Context

The backoffice application requires an authentication mechanism allowing users to log in with their email and password and receive proof of authentication.

The authentication system must:

* identify authenticated users;
* carry the user's identity and role;
* integrate with the current layered architecture (Route → Service → Repository);
* remain independent from the ORM and business logic;
* be compatible with a REST API.

The project already uses Argon2 for password hashing and SQLAlchemy 2 for persistence.

## Decision

The project uses **JSON Web Tokens (JWT)** as the authentication mechanism and the **PyJWT** library to generate and validate tokens.

The authentication flow is:

1. The user submits an email and password.
2. The application retrieves the user from the database.
3. The password is verified using the password hashing service (`verify_password`).
4. If authentication succeeds, a JWT is generated.
5. The token is returned to the client and will be included in future authenticated requests.

The JWT contains at least:

* the user identifier;
* the user's role;
* an expiration date.

The token is signed using the application's secret key.

## Consequences

### Advantages

* Stateless authentication suitable for REST APIs.
* No server-side session storage required.
* Easy to scale across multiple application instances.
* PyJWT is lightweight and framework-independent.
* The token logic remains isolated from Flask, preserving separation of concerns.
* Compatible with the project's layered architecture.

### Disadvantages

* JWTs cannot easily be revoked before they expire.
* If a user is deactivated after a token has been issued, the token remains valid until expiration unless protected routes verify the user's active status on every request.
* Secret key management becomes critical for application security.

## Logout behavior

The application exposes a `POST /auth/logout` endpoint.

Because JWT authentication is stateless, the endpoint does not invalidate issued tokens on the server. Logging out instructs the client to remove the stored token.

The security implications of this choice are described in the **Security Considerations** section.

## Alternatives Considered

### Session-based authentication

Session authentication stores user state on the server and identifies users through cookies.

Advantages:

* Easy session revocation.
* Immediate logout capability.
* User deactivation takes effect instantly.

Disadvantages:

* Requires server-side session storage.
* Less suitable for stateless REST APIs.
* More difficult to scale across multiple application instances.

### Flask-JWT-Extended

This library provides many JWT features directly integrated with Flask.

It was not selected because it tightly couples authentication with Flask, whereas the project architecture favors reusable, framework-independent components. PyJWT provides lower-level control while keeping the authentication logic separated from the web framework.

## Security Considerations

* Passwords are never stored or transmitted in plaintext.
* Password verification relies on the dedicated Argon2 password hashing service.
* Authentication failures always return a generic error message to prevent user enumeration.
* Password hashes are never included in any response.
* The application's secret key must be stored securely using environment variables and never hardcoded in the source code.
* With stateless JWT authentication, logging out consists of the client removing the token; no server-side session is maintained.
* A JWT remains valid until its expiration time, even if the user logs out. If a token is stolen, it can still be used until it expires because no token revocation mechanism (such as a blacklist) is implemented.
* Immediate token revocation is outside the scope of this project and may be implemented in the future if required.
