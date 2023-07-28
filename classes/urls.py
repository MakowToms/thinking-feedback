from django.urls import path, include

from .views import (
    list_students,
    view_passwords,
    edit_class,
    edit_class_name,
    edit_student,
    delete_student,
    add_student,
    delete_class,
    add_class,
    add_class_next,
)

urlpatterns = [
    path('', list_students),
    path('<int:pk>/passwords/', view_passwords),
    path('<int:pk>/edit/', edit_class),
    path('<int:pk>/edit/name/', edit_class_name),
    path('<int:pk1>/edit/<int:pk2>/', edit_student),
    path('<int:pk1>/edit/<int:pk2>/delete/', delete_student),
    path('<int:pk>/edit/add/', add_student),
    path('<int:pk>/edit/delete/', delete_class),
    path('add/', add_class),
    path('add/next/<int:pk>/', add_class_next),
]