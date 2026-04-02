class MSDynamics365CrmError(Exception):
    """class representing Generic Http error."""

    def __init__(self, message=None, response=None):
        super().__init__(message)
        self.message = message
        self.response = response


class MSDynamics365CrmBackoffError(MSDynamics365CrmError):
    """class representing backoff error handling."""
    pass

class MSDynamics365CrmBadRequestError(MSDynamics365CrmError):
    """class representing 400 status code."""
    pass

class MSDynamics365CrmUnauthorizedError(MSDynamics365CrmError):
    """class representing 401 status code."""
    pass

class MSDynamics365CrmForbiddenError(MSDynamics365CrmError):
    """class representing 403 status code."""
    pass

class MSDynamics365CrmNotFoundError(MSDynamics365CrmError):
    """class representing 404 status code."""
    pass

class MSDynamics365CrmMethodNotAllowedError(MSDynamics365CrmError):
    """class representing 405 status code."""
    pass

class MSDynamics365CrmPreconditionFailedError(MSDynamics365CrmError):
    """class representing 412 status code."""
    pass

class MSDynamics365CrmPayloadTooLargeError(MSDynamics365CrmError):
    """class representing 413 status code."""
    pass

class MSDynamics365CrmConflictError(MSDynamics365CrmError):
    """class representing 409 status code."""
    pass

class MSDynamics365CrmUnprocessableEntityError(MSDynamics365CrmError):
    """class representing 422 status code."""
    pass

class MSDynamics365CrmRateLimitError(MSDynamics365CrmBackoffError):
    """class representing 429 status code."""
    pass

class MSDynamics365CrmInternalServerError(MSDynamics365CrmBackoffError):
    """class representing 500 status code."""
    pass

class MSDynamics365CrmNotImplementedError(MSDynamics365CrmBackoffError):
    """class representing 501 status code."""
    pass

class MSDynamics365CrmBadGatewayError(MSDynamics365CrmBackoffError):
    """class representing 502 status code."""
    pass

class MSDynamics365CrmServiceUnavailableError(MSDynamics365CrmBackoffError):
    """class representing 503 status code."""
    pass

# MS Dynamics 365 Web API HTTP status code reference:
# https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/compose-http-requests-handle-errors
ERROR_CODE_EXCEPTION_MAPPING = {
    400: {
        "raise_exception": MSDynamics365CrmBadRequestError,
        "message": "Bad request. The request URL or body is invalid or malformed."
    },
    401: {
        "raise_exception": MSDynamics365CrmUnauthorizedError,
        "message": "Unauthorized. The access token is missing, expired, or invalid."
    },
    403: {
        "raise_exception": MSDynamics365CrmForbiddenError,
        "message": "Forbidden. The user does not have the required Dataverse security role or privilege to perform this operation."
    },
    404: {
        "raise_exception": MSDynamics365CrmNotFoundError,
        "message": "Not found. The requested resource or entity record does not exist."
    },
    405: {
        "raise_exception": MSDynamics365CrmMethodNotAllowedError,
        "message": "Method not allowed. The HTTP method used is not supported for this resource."
    },
    409: {
        "raise_exception": MSDynamics365CrmConflictError,
        "message": "Conflict. The operation conflicts with an existing record (duplicate detection or concurrency violation)."
    },
    412: {
        "raise_exception": MSDynamics365CrmPreconditionFailedError,
        "message": "Precondition failed. A condition specified in the request headers (e.g. If-Match) was not met."
    },
    413: {
        "raise_exception": MSDynamics365CrmPayloadTooLargeError,
        "message": "Payload too large. The request body exceeds the size limit allowed by the server."
    },
    422: {
        "raise_exception": MSDynamics365CrmUnprocessableEntityError,
        "message": "Unprocessable entity. The request was well-formed but could not be processed."
    },
    429: {
        "raise_exception": MSDynamics365CrmRateLimitError,
        "message": "Too many requests. Service Protection API limits exceeded. Retry after the period indicated in the Retry-After header."
    },
    500: {
        "raise_exception": MSDynamics365CrmInternalServerError,
        "message": "Internal server error. The server encountered an unexpected condition which prevented it from fulfilling the request."
    },
    501: {
        "raise_exception": MSDynamics365CrmNotImplementedError,
        "message": "Not implemented. The server does not support the functionality required to fulfill the request."
    },
    502: {
        "raise_exception": MSDynamics365CrmBadGatewayError,
        "message": "Bad gateway. An upstream proxy or load balancer received an invalid response from the MS Dynamics server."
    },
    503: {
        "raise_exception": MSDynamics365CrmServiceUnavailableError,
        "message": "Service unavailable. The MS Dynamics 365 API service is temporarily unavailable. Retry after a short delay."
    }
}
