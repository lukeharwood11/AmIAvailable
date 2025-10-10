import jwt
from datetime import datetime
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .database import get_supabase_admin_client
from typing import TypedDict, Any

import logging

logger = logging.getLogger(__name__)


class DebugHTTPBearer(HTTPBearer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        logger.info("=== HTTPBearer.__call__ invoked ===")
        logger.info("=== HTTPBearer.__call__ invoked ===")
        try:
            result = await super().__call__(request)
            logger.info(f"HTTPBearer success, got credentials: {result}")
            return result
        except Exception as e:
            logger.error(f"HTTPBearer failed: {str(e)}")
            logger.error(f"HTTPBearer exception type: {type(e)}")
            logger.info(f"DEBUG: HTTPBearer failed: {str(e)}")
            raise


async def verify_jwt(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> dict[str, Any]:
    """
    Verify JWT token using Supabase and cache user data in request state
    """
    try:
        token = credentials.credentials
        cache_key = f"user_data_{token[:20]}"
        if hasattr(request.state, cache_key):
            return getattr(request.state, cache_key)

        # Use Supabase admin client to verify the token
        supabase = get_supabase_admin_client()
        # Verify the JWT token
        response = supabase.auth.get_user(token)
        if not response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_data = {
            "user_id": response.user.id,
            "email": response.user.email,
            "user": response.user,
        }

        # Cache the user data in request state
        setattr(request.state, cache_key, user_data)

        return user_data

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )


class UserIdentityData(TypedDict, total=False):
    avatar_url: str
    email: str
    email_verified: bool
    full_name: str
    iss: str
    name: str
    phone_verified: bool
    picture: str
    provider_id: str
    sub: str


class UserIdentity(TypedDict):
    id: str
    identity_id: str
    user_id: str
    identity_data: UserIdentityData
    provider: str
    created_at: datetime
    last_sign_in_at: datetime
    updated_at: datetime


class UserMetadata(TypedDict, total=False):
    avatar_url: str
    email: str
    email_verified: bool
    full_name: str
    iss: str
    name: str
    phone_verified: bool
    picture: str
    provider_id: str
    sub: str


class AppMetadata(TypedDict):
    provider: str
    providers: list[str]


class UserTypedDict(TypedDict):
    id: str
    app_metadata: AppMetadata
    user_metadata: UserMetadata
    aud: str
    confirmation_sent_at: datetime | None
    recovery_sent_at: datetime | None
    email_change_sent_at: datetime | None
    new_email: str | None
    new_phone: str | None
    invited_at: datetime | None
    action_link: str | None
    email: str
    phone: str
    created_at: datetime
    confirmed_at: datetime | None
    email_confirmed_at: datetime | None
    phone_confirmed_at: datetime | None
    last_sign_in_at: datetime | None
    role: str
    updated_at: datetime
    identities: list[UserIdentity]
    is_anonymous: bool
    factors: list[str] | None  # can refine if MFA factors are typed


class UserContainer(TypedDict):
    user_id: str
    email: str
    user: UserTypedDict


async def get_current_user(
    auth_data: UserContainer = Depends(verify_jwt),
) -> UserContainer:
    """
    Get current authenticated user
    """
    return auth_data


async def get_current_user_id(auth_data: UserContainer = Depends(verify_jwt)) -> str:
    """
    Get current authenticated user ID
    """
    return auth_data["user_id"]


# Optional auth dependency (for endpoints that can work with or without auth)
async def get_optional_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(
        HTTPBearer(auto_error=False)
    ),
) -> dict[str, Any] | None:
    """
    Get current user if authenticated, None otherwise
    """
    if not credentials:
        return None

    try:
        return await verify_jwt(request, credentials)
    except HTTPException:
        return None
