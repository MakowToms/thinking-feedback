from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from classes.models import Stage
from exam.models import Test, StudentTest
from topic.models import Topic


@staff_member_required
def class_view(request, pk: int):
    stage = Stage.objects.filter(pk=pk).first()
    tests = Test.objects.filter(stage=pk).order_by("-date")
    student_tests = StudentTest.objects.filter(stage=pk).order_by("-date")

    topics = Topic.objects.filter(stage=stage)

    context = {
        "tests": tests, "student_tests": student_tests,
        "topics": topics,
        "chosen_stage": pk,
    }
    template_name = "class_view.html"
    return render(request, template_name, context)
