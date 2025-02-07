"""
URL configuration for auth.
"""

from django.urls import path
from .views.auth_login_view import AuthLoginView
from .views.auth_logout_view import AuthLogoutView
from .views.auth_refresh_view import AuthRefreshTokenView

urlpatterns = [
    path("login/", AuthLoginView.as_view(), name="auth-login"),
    path("logout/", AuthLogoutView.as_view(), name="auth-logout"),
    path("token/refresh/", AuthRefreshTokenView.as_view(), name="auth-refresh"),
]
