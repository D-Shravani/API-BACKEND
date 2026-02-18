"""
Response helper functions for consistent API responses
"""
from flask import jsonify


def success_response(data=None, message="Operation successful", status_code=200):
    """
    Create a standardized success response
    
    Args:
        data: Response data (dict, list, or None)
        message: Success message
        status_code: HTTP status code
    
    Returns:
        Flask response object
    """
    response = {
        "status": "success",
        "message": message
    }
    
    if data is not None:
        response["data"] = data
    
    return jsonify(response), status_code


def error_response(message, error_code="ERROR", status_code=400):
    """
    Create a standardized error response
    
    Args:
        message: Error message
        error_code: Error code identifier
        status_code: HTTP status code
    
    Returns:
        Flask response object
    """
    response = {
        "status": "error",
        "error_code": error_code,
        "message": message
    }
    
    return jsonify(response), status_code
