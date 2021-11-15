from django.contrib import admin
from django.urls import path

from api.views import (
    UserPositionDetails,
    UserPositionManager,
    GroupPositionDetails,
    UserDetails,
    UserManager,
    GroupDetails,
    GroupManager,
    GroupMembers,
)

urlpatterns = [
    path('position/', UserPositionManager.as_view()), #OK, TESTED
    path('position/<slug:pk>/', UserPositionDetails.as_view()), #OK, TESTED
    path('position/group/<slug:pk>/', GroupPositionDetails.as_view()), # NOT IMPLEMENTED
    path('user/', UserManager.as_view()), #OK, TESTED
    path('user/<slug:pk>/', UserDetails.as_view()), #OK, TESTED
    path('group/', GroupManager.as_view()), #OK, TESTED
    path('group/<slug:pk>/', GroupDetails.as_view()), #OK, TESTED
    path('group/<slug:pk>/members/', GroupMembers.as_view()), #OK, TESTED
]
