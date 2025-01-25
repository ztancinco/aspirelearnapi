"""
URLs for Dash users.
"""

from django.urls import path
from ..users.views.users_view import DashUsersView

urlpatterns = [
    path('', DashUsersView.as_view(), name='dash-user-list'),
]
