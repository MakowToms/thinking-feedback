from django.urls import path

from .views import (
    all_tables, all_tables_view,
)

urlpatterns = [
    path("", all_tables),
    path("<int:pk1>/", all_tables_view),
]
