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
def by_student(request):
    stages = Stage.objects.filter(teacher=request.user)
    students = {}
    for stage in stages:
        students[stage] = stage.students.all()
    context = {"students": students, "empty": 0}
    if len(stages) == 0:
        context["empty"] = 1
    template_name = "by_student.html"
    return render(request, template_name, context)


@staff_member_required
def by_student_view(request, pk1):
    student = User.objects.get(pk=pk1)
    stage = student.classes.all()[0]
    if stage.teacher != request.user:
        return redirect("/")
    topics = Topic.objects.filter(stage=stage)
    student_data = {}
    all_tables = ""
    for topic in topics:
        table = "Dział " + topic.title + ": \n"
        skill_list = Skill.objects.filter(topic=topic).order_by("order")
        grades = {}
        for skill in skill_list:
            all_grades = Grade.objects.filter(student=student, skill_level__in=skill.levels.all()).all()
            skill_table, skill_grades = convert_grades_to_table(all_grades)
            grades[skill.title] = skill_grades
            table += f"{skill.title}: {skill_table}\n"
        all_tables += table
        student_data[topic.title] = {
            'grades': grades,
            'table': table + LEGEND,
        }
    context = {
        "student": student,
        "data": student_data,
        "all_table": all_tables,
    }
    template_name = "by_student_view.html"

    return render(request, template_name, context)


@staff_member_required
def by_student_view_old(request, pk1):
    student = User.objects.get(pk=pk1)
    stage = student.classes.all()[0]
    if stage.teacher != request.user:
        return redirect("/")
    topics = Topic.objects.filter(stage=stage)
    topic_grades = {}
    context = {
        "student": student,
    }
    topic_tables = {}
    table = ""
    for topic in topics:
        topic_table = "Dział " + topic.title + ": \n"
        skill_list = Skill.objects.filter(topic=topic).order_by("order")
        grades = {}
        student = User.objects.get(pk=pk1)
        for skill in skill_list:
            topic_table += skill.title + ": "
            grades[skill] = []
            levels = {}
            for level in skill.levels.all():
                levels[level.level] = []
                temp = Grade.objects.filter(student=student, skill_level=level).order_by("publish_date")
                for grade in temp:
                    levels[level.level].append(grade)
            passed_levels = get_passed_levels(levels)
            max_passed_level = 0
            if len(passed_levels) > 0:
                max_passed_level = max(passed_levels)
            for level, g in sorted(levels.items(), key=lambda x: x[0]):
                if int(level) <= max_passed_level:
                    g.append(Grade(value="(zal)", publish_date=now()))
                grades[skill].append(g)
                if len(g) > 0 and g[-1].value == "(zal)":
                    topic_table += f"(p{level}: ZAL);"
                else:
                    topic_table += f"(p{level}: " + ", ".join([convert_grade(grade) for grade in g]) + "); "
            topic_table += "\n"

            topic_grades[topic.title] = grades
            topic_tables[topic.title] = topic_table + LEGEND
            table += topic_table
    table += LEGEND
    context["grades"] = topic_grades
    context["table"] = table
    context["topic_tables"] = topic_tables
    print(context)
    template_name = "by_student_view_old.html"
    return render(request, template_name, context)


def get_tables_to_grade_conversion(pk1, skill_ids=None):
    stage = Stage.objects.filter(id=pk1).first()
    data = defaultdict(lambda: defaultdict(lambda: 0))
    if skill_ids is None:
        ids = {0}
        for student in sorted(stage.students.all(), key=lambda s: (s.last_name, s.first_name)):
            grades = Grade.objects.filter(student__pk=student.id).all()
            for grade in grades:
                ids.add(grade.skill_level.skills.first().id)
        print(ids)
    else:
        skills = Skill.objects.filter(id__in=skill_ids)
        for student in sorted(stage.students.all(), key=lambda s: (s.last_name, s.first_name)):
            results = []
            table = ""
            for skill in skills:
                table += skill.title + ": "
                levels = {}
                for level in skill.levels.all():
                    levels[level.level] = []
                    temp = Grade.objects.filter(student=student, skill_level=level).order_by("publish_date")
                    for grade in temp:
                        levels[level.level].append(grade)
                passed_levels = get_passed_levels(levels, 1)
                max_passed_level = 0
                if len(passed_levels) > 0:
                    max_passed_level = max(passed_levels)
                data[student.first_name + student.last_name][skill.title] = max_passed_level
                results.append(max_passed_level)
                for level, g in sorted(levels.items(), key=lambda x: x[0]):
                    if int(level) <= max_passed_level:
                        g.append(Grade(value="(zal)", publish_date=now()))
                    if len(g) > 0 and g[-1].value == "(zal)":
                        table += f"(p{level}: ZAL);"
                    else:
                        table += f"(p{level}: " + ", ".join([convert_grade(grade) for grade in g]) + "); "
                table += "\n "
            grade = 1
            results = sorted(results)
            if results[0] == 3:
                grade = 6
            elif results[0] == 2:
                if results[int(0.3*len(results))] == 3:
                    grade = 6
                else:
                    grade = 5
            elif results[0] == 1:
                if results[int(0.3*len(results))] >= 2:
                    grade = 4
                else:
                    grade = 3
            elif results[0] == 0:
                if results[int(0.3*len(results))] >= 1:
                    grade = 2
                else:
                    grade = 1
            print("\n\n", student.first_name + student.last_name)
            print(grade)
            print(table)


@staff_member_required
def by_student_update(request, pk1, pk2):
    obj = get_object_or_404(Topic, pk=pk2)
    student = User.objects.get(pk=pk1)
    stage = student.classes.all()[0]
    if stage.teacher != request.user:
        return redirect("/")
    skill_list = Skill.objects.filter(topic=obj)
    context = {"student": student, "skill_list": skill_list, "topic": obj.title}
    template_name = "by_student_update.html"
    if request.POST:
        for key, value in request.POST.items():
            if key != "csrfmiddlewaretoken" and value != "empty":
                skill_pk = key[:-1]
                skill = Skill.objects.get(topic=obj, pk=skill_pk)
                level = key[-1]
                grade = Grade(student=student, skill=skill, value=value, level=level)
                grade.save()
        return redirect("..")
    return render(request, template_name, context)


@staff_member_required
def by_student_edit(request, pk1, pk2):
    student = User.objects.get(pk=pk1)
    stage = student.classes.all()[0]
    if stage.teacher != request.user:
        return redirect("/")
    obj = get_object_or_404(Topic, pk=pk2)
    skill_list = Skill.objects.filter(topic=obj)
    context = {
        "skill_list": skill_list,
        "student": student,
        "topic": obj.title,
    }
    grades = {}
    student = User.objects.get(pk=pk1)
    for skill in skill_list:
        grades[skill] = {}
        for level in (1, 2, 3):
            temp_grades = []
            temp = Grade.objects.filter(student=student, skill=skill, level=level)
            for grade in temp:
                temp_grades.append(grade)
            if len(temp_grades) > 1:
                grades[skill][level] = (temp_grades[:-1], temp_grades[-1])
            elif len(temp_grades) == 1:
                grades[skill][level] = ([], temp_grades[0])
            else:
                grades[skill][level] = ([], "")

    context["grades"] = grades
    template_name = "by_student_edit.html"

    if request.POST:
        for key, value in request.POST.items():
            if key != "csrfmiddlewaretoken":
                skill_pk = key[:-1]
                skill = Skill.objects.get(topic=obj, pk=skill_pk)
                level = key[-1]
                grade = Grade.objects.filter(
                    student=student, skill=skill, level=level,
                ).last()
                if value == "empty":
                    grade.delete()
                elif grade.value != value:
                    grade.value = value
                    grade.save()
        return redirect("..")

    return render(request, template_name, context)
