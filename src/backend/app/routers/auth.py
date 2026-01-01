"""Authentication router for Phase II Todo Application."""
from fastapi import APIRouter, HTTPException, status
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
import uuid

from app.schemas.auth import SignUpRequest, SignInRequest, TokenResponse
from app.db.config import get_session
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

BETTER_AUTH_SECRET = os.environ.get("BETTER_AUTH_SECRET", "your-secret-key")

def create_jwt_token(user_id: str, email: str) -> str:
    expire = datetime.utcnow() + timedelta(days=7)
    payload = {
        "sub": user_id,
        "email": email,
        "exp": expire,
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, BETTER_AUTH_SECRET, algorithm="HS256")


@router.post("/sign-up", response_model=TokenResponse)
async def sign_up(request: SignUpRequest):
    session = next(get_session())
    try:
        existing = session.query(User).filter(User.email == request.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        user = User(
            id=str(uuid.uuid4()),
            email=request.email,
            name=request.name,
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        token = create_jwt_token(user.id, user.email)
        return TokenResponse(
            token=token,
            user_id=user.id,
            email=user.email
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )
    finally:
        session.close()


@router.post("/sign-in", response_model=TokenResponse)
async def sign_in(request: SignInRequest):
    session = next(get_session())
    try:
        user = session.query(User).filter(User.email == request.email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        token = create_jwt_token(user.id, user.email)
        return TokenResponse(
            token=token,
            user_id=user.id,
            email=user.email
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Sign in failed: {str(e)}"
        )
    finally:
        session.close()


@router.get("/verify", response_model=TokenResponse)
async def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )
        return TokenResponse(
            token=token,
            user_id=payload.get("sub", ""),
            email=payload.get("email", "")
        )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )
