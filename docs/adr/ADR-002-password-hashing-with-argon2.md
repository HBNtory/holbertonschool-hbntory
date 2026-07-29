# ADR-002: Password hashing with Argon2id

## Status
Accepted

## Context
The backoffice stores user accounts and must handle passwords securely. Storing
passwords in plain text is unacceptable, and a general-purpose hash like SHA-256
is not enough on its own (see Consequences). We need a mechanism designed for
password storage, and it must be usable both by the app and by the seed script,
so it is written as pure functions independent of Flask.

Three common mechanisms were considered: bcrypt, Argon2 and PBKDF2.

## Decision
We use **Argon2id**, via the `argon2-cffi` library, exposed as two pure functions
in `app/utils/security.py`: `hash_password` and `verify_password`.

Argon2id was chosen because it is the current reference recommendation for
password storage (e.g. OWASP). Unlike bcrypt and PBKDF2, which only stress the
CPU, Argon2 is also memory-hard, which makes GPU/ASIC brute-force attacks harder.

The hashing parameters (memory, time, parallelism) use the library defaults,
which follow current recommendations.

## Consequences
Positive:
- The salt and all parameters are embedded in the hash string itself
  (`$argon2id$...`), so verification needs only the password and the stored hash
  — no separate salt handling.
- A random salt per password means two identical passwords produce different
  hashes, defeating rainbow tables.
- The functions are framework-agnostic, so the seed can reuse them outside Flask.

Why a plain hash like SHA-256 is not sufficient:
- SHA-256 is built to be fast. Speed is a weakness for password storage: an
  attacker who steals the database can try billions of guesses per second
  (brute-force / dictionary attacks).
- On its own it is unsalted, so identical passwords hash identically and rainbow
  tables apply.
- Password-hashing mechanisms are deliberately slow, tunable and salted to
  resist these attacks.

Trade-offs:
- Argon2 is more recent than bcrypt, so less battle-tested by time (but it is the
  current recommended standard).
- Hashing is intentionally slow, which is the point, but means each login/verify
  costs measurable CPU and memory — acceptable for a backoffice.