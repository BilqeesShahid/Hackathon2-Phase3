"""JWT authentication middleware for FastAPI."""
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from pydantic import BaseModel
from typing import Optional
import os

# Load environment
BETTER_AUTH_SECRET = os.environ.get("BETTER_AUTH_SECRET", "")

security = HTTPBearer()


class CurrentUser(BaseModel):
    """User information extracted from JWT."""
    user_id: str
    email: Optional[str] = None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> CurrentUser:
    """
    Validate JWT token and extract user information.

    Args:
        credentials: HTTP Bearer token from Authorization header

    Returns:
        CurrentUser with user_id and email from token

    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )

        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return CurrentUser(
            user_id=user_id,
            email=payload.get("email")
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def verify_user_access(
    user_id: str,
    current_user: CurrentUser = Depends(get_current_user)
) -> str:
    """
    Verify that the authenticated user matches the requested user ID.

    Args:
        user_id: The user ID from the request path
        current_user: The authenticated user from JWT

    Returns:
        The verified user ID

    Raises:
        HTTPException: If user ID doesn't match
    """
    if user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's resources"
        )
    return user_id
