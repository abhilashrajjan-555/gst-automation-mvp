"""
Authentication middleware for FastAPI
Verifies JWT tokens from Supabase
"""

import jwt
import os
from fastapi import HTTPException, Header
from typing import Optional

# Get Supabase JWT secret from environment
SUPABASE_JWT_SECRET = os.getenv('SUPABASE_JWT_SECRET', '')

def verify_token(authorization: Optional[str] = Header(None)) -> dict:
    """
    Verify JWT token from Authorization header
    
    Args:
        authorization: Bearer token from request header
        
    Returns:
        Decoded token payload with user info
        
    Raises:
        HTTPException: If token is invalid or missing
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="No authorization header")
    
    try:
        # Extract token from "Bearer <token>"
        scheme, token = authorization.split()
        if scheme.lower() != 'bearer':
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
        
        # Decode and verify token
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated"
        )
        
        return payload
        
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

def get_user_id(authorization: Optional[str] = Header(None)) -> str:
    """
    Extract user ID from JWT token
    
    Args:
        authorization: Bearer token from request header
        
    Returns:
        User ID (UUID string)
    """
    payload = verify_token(authorization)
    user_id = payload.get('sub')
    
    if not user_id:
        raise HTTPException(status_code=401, detail="No user ID in token")
    
    return user_id
