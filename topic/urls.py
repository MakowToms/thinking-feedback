from django.urls import path

from topic.views import (
    add_skill, add_topic, stage_all_topics, delete_topic,
    skill_delete, skill_edit, topic_detail_view,
    update_topic, add_skill_level,
)

urlpatterns = [
    path("", stage_all_topics),
    path("add/", add_topic),
    path("<int:pk>/", topic_detail_view),
    path("<int:pk1>/skill/<int:pk2>/edit/", skill_edit),
    path("<int:pk1>/skill/<int:pk2>/delete/", skill_delete),
    path("<int:pk1>/skill/<int:pk2>/add_skill_level/", add_skill_level),
    path("<int:pk>/add/", add_skill),
    path("<int:pk>/edit/", update_topic),
    path("<int:pk>/delete/", delete_topic),
]
