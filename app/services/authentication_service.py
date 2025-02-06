"""
Service for authentication.

This service class handles actions related to authentication, such as validating
JWT tokens and managing route access for requests.
"""

import os
import logging
from typing import List, Optional
from dotenv import load_dotenv
from django.urls import get_resolver, Resolver404
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

load_dotenv()
logger = logging.getLogger(__name__)

class AuthenticationService:
    """
    Service class for handling authentication-related operations.
    """

    def __init__(self) -> None:
        """
        Initialize the AuthenticationService with routes and excluded routes.
        """
        self.routes: List[str] = self.get_all_routes()
        self.api_version: str = os.getenv('DJANGO_API_VERSION', 'v1')
        self.excluded_routes: List[str] = [
            f'/api/{self.api_version}/auth/login',
            f'/api/{self.api_version}/auth/logout'
        ]
        logger.debug("Initialized AuthenticationService with routes: %s", self.routes)

    def get_all_routes(self) -> List[str]:
        """
        Retrieve all URL patterns in the project and return them as a list of strings.

        :return: A list of all registered URL patterns.
        """
        try:
            url_patterns = get_resolver().url_patterns
            routes: List[str] = []

            def extract_routes(patterns: List, parent_pattern: str = '') -> None:
                for pattern in patterns:
                    if hasattr(pattern, 'url_patterns'):
                        # Recursive call for nested URL patterns
                        extract_routes(
                            pattern.url_patterns,
                            parent_pattern + str(pattern.pattern)
                        )
                    else:
                        # Append full pattern to the routes list
                        routes.append(parent_pattern + str(pattern.pattern))

            extract_routes(url_patterns)
            return routes

        except Resolver404:
            logger.error("URL resolver not found.")
            return []

    def authenticate_request(self, request: HttpRequest) -> Optional[HttpResponse]:
        """
        Authenticate the request using JWT and check if the user is authenticated.

        :param request: Django HttpRequest object.
        :return: HttpResponseForbidden if authentication fails, otherwise None.
        """
        if request.path.startswith('/api/') and not any(
            request.path.startswith(excluded_route)
            for excluded_route in self.excluded_routes
        ):
            jwt_auth: JWTAuthentication = JWTAuthentication()
            auth_header: Optional[str] = request.headers.get('Authorization')

            if auth_header:
                try:
                    prefix, token = auth_header.split(' ')
                    if prefix == 'Bearer':
                        logger.debug("Bearer token found, attempting validation.")
                        validated_token = jwt_auth.get_validated_token(token)
                        request.user = jwt_auth.get_user(validated_token)

                    if not request.user.is_authenticated:
                        return HttpResponseForbidden(
                            "You do not have permission to access this resource."
                        )
                except (InvalidToken, TokenError) as e:
                    logger.error("Authentication error: %s", e)
                    return HttpResponseForbidden("Invalid or expired token.")
            else:
                logger.warning("No Authorization header provided.")
                return HttpResponseForbidden("Authorization credentials not provided.")
        return None

    def process_request(self, request: HttpRequest) -> Optional[HttpResponse]:
        """
        Process the request to ensure proper authentication and route access.

        :param request: Django HttpRequest object.
        :return: HttpResponseForbidden if authentication fails, otherwise None.
        """
        return self.authenticate_request(request)
