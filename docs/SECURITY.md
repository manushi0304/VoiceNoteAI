# VoiceNote AI: Security Policies & Implementation

This document details the security principles, data protection designs, and cryptographic libraries incorporated into the VoiceNote AI system.

---

## 🔑 1. User Authentication & Cryptography

### Hashed Passwords (`bcrypt`)
- Passwords are never stored in plain text.
- Passwords are encrypted using high-entropy `bcrypt` hashing algorithms provided by the `passlib` crypt library.
- Hashing is performed in `AuthService.register()` before committing records to the relational database.
- Verification is performed using crypt secure comparisons inside `AuthService.authenticate()`.

### JSON Web Tokens (JWT)
- Sessions are completely stateless and authenticated via JWT access tokens.
- Cryptographic signature generation and verification are handled by the `python-jose` library.
- Access tokens expire automatically after **30 minutes** (configured via `.env` parameter `ACCESS_TOKEN_EXPIRE_MINUTES`).
- Token signature hashes use `HS256` utilizing a high-entropy crypt key (`JWT_SECRET`).

---

## 🛡️ 2. Route Protection & Authorization

### Dependency Injection
- API route handlers enforce authentication via FastAPI's `Depends(get_current_user)` dependency injection.
- `get_current_user` performs:
  1. Extraction of the bearer token from the HTTP `Authorization` header.
  2. Cryptographic signature and expiration checks.
  3. Relational querying to verify that the target User exists and is active.
- Unauthenticated requests are rejected immediately with a `401 Unauthorized` response code.

### Database Row-Level Sandboxing
- Multi-tenancy is enforced. Relational queries in `notes`, `todos`, and `reminders` services always isolate results by scoping on the user's validated database ID (`user_id`).
- It is impossible for an authenticated user to view, edit, or delete another user's private data.

---

## 🔒 3. Network & Transport Security

### CORS (Cross-Origin Resource Sharing)
- FastAPI mounts standard `CORSMiddleware` to prevent unauthorized cross-domain scripting attacks.
- Allowed origins are strictly restricted in `main.py` to local Streamlit presentation domains:
  - `http://localhost:8501`
  - `http://127.0.0.1:8501`
  - `http://localhost:3000`
  - `http://127.0.0.1:3000`
- Prevents malicious websites from executing cross-domain requests on behalf of logged-in users.

### Environment Enforce
- Sensitive credentials (such as database URLs, JWT secret keys, and SMTP server passcodes) are excluded from the codebase and loaded exclusively via local environment configurations (`.env`) loaded at server boot time.
