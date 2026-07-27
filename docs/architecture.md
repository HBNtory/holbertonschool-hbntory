### Backoffice architecture
The backoffice is a Flask app organized with an application factory and
blueprints (one blueprint per resource). Business code is layered:
```
route (HTTP) -> service (business logic) -> repository (ORM access) -> DB
```
- **route**: handles HTTP, validates input/output with pydantic, calls the
  service, translates business exceptions into status codes.
- **service**: business rules; receives a repository (dependency injection),
  contains no ORM code, raises business exceptions instead of returning HTTP.
- **repository**: the only place that talks to the ORM (SQLAlchemy).
- **Utils**: pure, stateless helper functions (e.g. password hashing), no DB
  access, reusable outside Flask.

Each layer only knows the one below it: routes never run SQL, the repository
never knows HTTP exists.

### Data models
- SQLAlchemy models for persistence, pydantic schemas for validation and
  serialization (Create / Update / Read per resource).
- Output schemas never expose sensitive fields (e.g. password hashes).