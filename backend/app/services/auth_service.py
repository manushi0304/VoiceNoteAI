from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.auth import UserCreate
from app.core.security import (
    get_password_hash,
    verify_password,
)

class AuthService:
    """
    Handles user authentication & registration logic.
    Does NOT create JWT tokens directly (API layer does that).
    """

    # --------------------------------------------------
    # Register a new user
    # --------------------------------------------------
    @staticmethod
    async def register(
        db: AsyncSession,
        user_in: UserCreate,
    ):
        # Check if user already exists
        result = await db.execute(
            select(User).where(User.email == user_in.email)
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Create user
        user = User(
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            full_name=user_in.full_name,
            is_active=True,
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        return {
            "id": str(user.id),
            "email": user.email,
        }

    # --------------------------------------------------
    # Authenticate user (used by OAuth2 login)
    # --------------------------------------------------
    @staticmethod
    async def authenticate(
        db: AsyncSession,
        email: str,
        password: str,
    ) -> User | None:
        result = await db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()

        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user
