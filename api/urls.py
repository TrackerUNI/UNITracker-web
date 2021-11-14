from django.contrib import admin
from django.urls import path

from api.views import (
    UserPositionDetails,
    UserPositionManager,
    GroupPositionDetails,
    GroupPositionManager,
    UserDetails,
    UserManager,
    GroupDetails,
    GroupManager,
    GroupMembers,
)

urlpatterns = [
    path('position/', UserPositionManager.as_view()), #OK
    path('position/<slug:pk>/', UserPositionDetails.as_view()), #OK
    #path('position/group/', GroupPositionManager.as_view()),
    path('position/group/<slug:pk>/', GroupPositionDetails.as_view()),
    path('user/', UserManager.as_view()), #OK
    path('user/<slug:pk>/', UserDetails.as_view()), #OK
    path('group/', GroupManager.as_view()), #OK
    path('group/<slug:pk>/', GroupDetails.as_view()), #OK
    path('group/<slug:pk>/members/', GroupMembers.as_view()), #OK
]
