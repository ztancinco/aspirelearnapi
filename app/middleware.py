"""
Middleware to guard routes
"""

from django.utils.deprecation import MiddlewareMixin
from app.services.authentication_service import AuthenticationService
from app.services.logger_service import LoggerService


class DynamicRouteGuardMiddleware(MiddlewareMixin):
    """
    Middleware to guard routes dynamically based on authentication service.
    """

    def __init__(self, get_response):
        """
        Initialize the middleware with the response handler, authentication service, and logger.
        """
        super().__init__(get_response)
        self.auth_service = AuthenticationService()
        self.logger = LoggerService(name='DynamicRouteGuardMiddleware', log_file='middleware.log')
        self.logger.get_logger().debug("DynamicRouteGuardMiddleware initialized")

    def __call__(self, request):
        """
        Handle the incoming request and pass it through the authentication service.
        """
        logger = self.logger.get_logger()
        logger.debug("Request path: %s", request.path)

        # Process the request through the authentication service
        response = self.auth_service.process_request(request)
        if response:
            return response

        response = self.get_response(request)
        logger.debug("Response status: %s", response.status_code)
        return response
