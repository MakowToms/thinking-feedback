from django.urls import path

from .views import (class_view)

urlpatterns = [
    path("<int:pk>/", class_view),
]
