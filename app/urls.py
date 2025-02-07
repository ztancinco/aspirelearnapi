"""
URL configuration for the AspireLearn api.
"""

import os
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from dotenv import load_dotenv
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

load_dotenv()

API_VERSION = os.getenv("API_VERSION", "v1")

urlpatterns = [
    # API Endpoints
    path("admin/", admin.site.urls),
    path(f"api/{API_VERSION}/auth/", include("app.authentication.urls")),
    path(f"api/{API_VERSION}/users/", include("app.users.urls")),
    path(f"api/{API_VERSION}/courses/", include("app.courses.urls")),
    # Swagger & ReDoc
    path(f"api/{API_VERSION}/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        f"api/{API_VERSION}/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        f"api/{API_VERSION}/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
