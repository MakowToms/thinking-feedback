from collections import defaultdict

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now

from by_student.grade_utils import get_passed_levels, convert_grade, LEGEND, convert_grades_to_table
from classes.models import Stage
from topic.models import Topic, Skill
from grade.models import Grade


# Create your views here.
@staff_member_required
def all_tables(request):
    stages = Stage.objects.filter(teacher=request.user).all()
    context = {"stages": stages, "empty": 0}
    if len(stages) == 0:
        context["empty"] = 1
    template_name = "all_tables.html"
    return render(request, template_name, context)


@staff_member_required
def all_tables_view(request, pk1):
    stage = Stage.objects.get(pk=pk1)
    if stage.teacher != request.user:
        return redirect("/")
    students = stage.students.order_by('last_name').all()
    topics = Topic.objects.filter(stage=stage).all()
    students_data = {}
    for student in students:
        #TODO student order
        whole_table = ""
        grades = {}
        for topic in topics:
            table = "Dział " + topic.title + ": \n"
            skill_list = Skill.objects.filter(topic=topic).order_by("order")
            # TODO remove below 71, 72, 69
            skill_list = [s for s in skill_list if s.pk not in [10, 11, 12, 13, 16, 25, 28, 29, 30, 31, 36, 73, 74, 75, ]]
            for skill in skill_list:
                all_grades = Grade.objects.filter(student=student, skill_level__in=skill.levels.all()).all()
                skill_table, skill_grades = convert_grades_to_table(all_grades)
                grades[skill.title] = skill_grades
                table += f"{skill.title}: {skill_table}\n"
            whole_table += table
        students_data[student] = {
            'grades': grades,
            'table': whole_table + LEGEND,
        }
    context = {
        "stage": stage,
        "data": students_data,
    }
    template_name = "all_tables_view.html"

    return render(request, template_name, context)
#
# for skill in Skill.objects.filter(topic__stage_id=3):
#     print(skill.pk, skill.title)
