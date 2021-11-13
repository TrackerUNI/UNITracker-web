from django.contrib import admin
from django.urls import path

from api.views import (
    PositionDetail,
    PositionManager
)

urlpatterns = [
    path('', PositionManager.as_view()),
    path('<slug:pk>/', PositionDetail.as_view())
]
