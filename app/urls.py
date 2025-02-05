"""
URL configuration for the AspireLearn api.
"""

import os
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from dotenv import load_dotenv

load_dotenv()

API_VERSION = os.getenv('API_VERSION', 'v1')

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'api/{API_VERSION}/auth/', include('app.authentication.urls')),
    path(f'api/{API_VERSION}/users/', include('app.users.urls')),
    path(f'api/{API_VERSION}/courses/', include('app.courses.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
