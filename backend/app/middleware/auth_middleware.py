from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError

from app.core.config import settings


class AuthMiddleware(BaseHTTPMiddleware):
    """
    HTTP authentication middleware.

    IMPORTANT:
    - WebSockets MUST be skipped
    - Auth is enforced only for HTTP routes
    """

    async def dispatch(self, request: Request, call_next):
        # 🔥 VERY IMPORTANT: NEVER touch WebSockets
        if request.scope["type"] == "websocket":
            return await call_next(request)

        # 🔹 Public routes (no auth)
        public_paths = [
            "/docs",
            "/openapi.json",
            "/health",
            "/auth/login",
            "/auth/register",
        ]

        if any(request.url.path.startswith(p) for p in public_paths):
            return await call_next(request)

        # 🔹 Read Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return await call_next(request)  # Let route-level deps handle auth

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM],
            )
            request.state.user_id = payload.get("sub")
        except JWTError:
            request.state.user_id = None

        return await call_next(request)
