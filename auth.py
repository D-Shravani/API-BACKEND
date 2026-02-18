"""
Authentication and authorization utilities
"""
from functools import wraps
from flask import request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from responses import error_response


def admin_required():
    """
    Decorator to require admin role for accessing an endpoint
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # Verify JWT is present and valid
            verify_jwt_in_request()
            
            # Get the JWT claims
            claims = get_jwt()
            role = claims.get("role", "user")
            
            # Check if user has admin role
            if role != "admin":
                return error_response(
                    message="Admin access required. You do not have permission to perform this action.",
                    error_code="FORBIDDEN",
                    status_code=403
                )
            
            return fn(*args, **kwargs)
        return decorator
    return wrapper


def jwt_required_custom():
    """
    Custom JWT required decorator with better error handling
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
                return fn(*args, **kwargs)
            except Exception as e:
                error_message = str(e)
                
                # Provide more specific error messages
                if "expired" in error_message.lower():
                    return error_response(
                        message="Token has expired. Please login again.",
                        error_code="TOKEN_EXPIRED",
                        status_code=401
                    )
                elif "signature" in error_message.lower():
                    return error_response(
                        message="Invalid token signature.",
                        error_code="INVALID_TOKEN",
                        status_code=401
                    )
                else:
                    return error_response(
                        message="Authentication required. Please provide a valid token.",
                        error_code="UNAUTHORIZED",
                        status_code=401
                    )
        return decorator
    return wrapper


def get_current_user_info():
    """
    Get current authenticated user information from JWT
    
    Returns:
        Dictionary containing user_id, email, and role
    """
    claims = get_jwt()
    identity = get_jwt_identity()  # This is now the user_id as a string
    
    return {
        "user_id": int(identity),
        "email": claims.get("email"),
        "role": claims.get("role", "user")
    }
