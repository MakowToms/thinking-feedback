from django.urls import path

from .views import (
    by_student, by_student_edit,
    by_student_update, by_student_view, by_student_view_old,
)

urlpatterns = [
    path("", by_student),
    path("<int:pk1>/", by_student_view),
    path("old/<int:pk1>/", by_student_view_old),
    path("<int:pk1>/topic/<int:pk2>/update/", by_student_update),
    path("<int:pk1>/topic/<int:pk2>/edit/", by_student_edit),
]
