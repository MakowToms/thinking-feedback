from collections import defaultdict

import numpy as np
import pandas as pd
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.timezone import now


# Create your views here.
from by_student.grade_utils import get_passed_levels, convert_grade, LEGEND, convert_grades_to_table
from classes.models import Stage
from grade.models import Grade
from topic.models import Topic, Skill


@staff_member_required
def by_topic(request):
    stages = Stage.objects.filter(teacher=request.user)
    topics = {}
    for stage in stages:
        topics[stage] = stage.topic_set.all()
    context = {"stages_to_topics": topics, "empty": 0}
    if len(stages) == 0:
        context["empty"] = 1
    template_name = "by_topic.html"
    return render(request, template_name, context)

@staff_member_required
def by_topic_view(request, pk1):
    topic = Topic.objects.get(pk=pk1)
    stage = topic.stage
    if stage.teacher != request.user:
        return redirect("/")
    students = stage.students.all()
    student_data = {}
    for student in students:
        table = "Dział " + topic.title + ": \n"
        skill_list = Skill.objects.filter(topic=topic).order_by("order")
        # TODO remove below
        skill_list = [s for s in skill_list if s.pk != 36]
        grades = {}
        for skill in skill_list:
            all_grades = Grade.objects.filter(student=student, skill_level__in=skill.levels.all()).all()
            skill_table, skill_grades = convert_grades_to_table(all_grades)
            grades[skill.title] = skill_grades
            table += f"{skill.title}: {skill_table}\n"
        student_data[student.get_full_name()] = {
            'grades': grades,
            'table': table + LEGEND,
        }
    context = {
        "topic": topic,
        "data": student_data,
    }
    template_name = "by_topic_view.html"

    return render(request, template_name, context)
