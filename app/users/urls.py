"""
URLs for Dash users.
"""

from django.urls import path
from ..users.views.users_view import UsersView

urlpatterns = [
    path('', UsersView.as_view(), name='users-list'),
]
