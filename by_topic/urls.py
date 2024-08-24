from django.urls import path

from .views import (
    by_topic, by_topic_view,
)

urlpatterns = [
    path("", by_topic),
    path("<int:pk1>/", by_topic_view),
]
