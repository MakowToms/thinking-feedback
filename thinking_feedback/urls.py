"""
URL configuration for website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("users.urls")),
    path("your_classes/", include("classes.urls")),
    path("student/", include("student_view.urls")),
    path("by_student/", include("by_student.urls")),
    path("by_topic/", include("by_topic.urls")),
    path("all_tables/", include("all_tables.urls")),
    path("topic/", include("topic.urls")),
    path("topic/", include("task.urls")),
    path("grade/", include("grade.urls")),
    path("test/", include("exam.urls")),
    path("class/", include("class_view.urls")),
]
