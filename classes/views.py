from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User

from users.models import Stage, Your_Stage, Initial_Password
from topic.forms import StageEditForm, StudentForm
# Create your views here.
context = {}

@staff_member_required
def list_students(request):
    stages   = Stage.objects.filter(teacher=request.user)
    students = {}
    for stage in stages:
        temp = Your_Stage.objects.filter(stage=stage)
        std  = User.objects.filter(your_stage__in=temp)
        students[stage] = std
    context['students'] = students
    context['empty'] = 0
    if len(students) == 0:
        context['empty'] = 1
    template_name = 'list_students.html'
    return render(request, template_name, context)

@staff_member_required
def view_passwords(request, pk):
    stage = Stage.objects.get(pk=pk, teacher=request.user)
    your_stages = Your_Stage.objects.filter(stage=stage)
    students = User.objects.filter(your_stage__in=your_stages)
    passwords = Initial_Password.objects.filter(student__in=students)
    context = {'stage': stage, 'passwords': passwords} 
    template_name = 'view_passwords.html'
    return render(request, template_name, context)

@staff_member_required
def edit_class(request, pk):
    stage = get_object_or_404(Stage, pk=pk, teacher=request.user)
    your_stages = Your_Stage.objects.filter(stage=stage)
    students = User.objects.filter(your_stage__in=your_stages)
    template_name = 'edit_class.html'
    context = {'stage': stage, 'students': students}
    return render(request, template_name, context)

@staff_member_required
def edit_class_name(request, pk):
    stage = get_object_or_404(Stage, pk=pk, teacher=request.user)
    form = StageEditForm(request.POST or None, instance=stage)
    if form.is_valid():
        form.save()
        return redirect('/your_classes')
    template_name = 'form.html'
    context = {'form': form}
    return render(request, template_name, context)

@staff_member_required
def edit_student(request, pk1, pk2):
    stage = get_object_or_404(Stage, pk=pk1, teacher=request.user)
    student = get_object_or_404(User, pk=pk2)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('/your_classes')
    template_name = 'form.html'
    context = {'form': form}
    return render(request, template_name, context)

@staff_member_required
def delete_student(request, pk1, pk2):
    stage = get_object_or_404(Stage, pk=pk1, teacher=request.user)
    student = get_object_or_404(User, pk=pk2)
    if request.method == "POST":
        student.delete()
        return redirect('/your_classes')
    template_name = 'delete_student.html'
    context = {'stage': stage, 'student': student}
    return render(request, template_name, context)

@staff_member_required
def add_student(request, pk):
    stage = get_object_or_404(Stage, pk=pk, teacher=request.user)
    form = StudentForm(request.POST or None)
    if form.is_valid():
        student = form.save(commit=False)
        first_name = student.first_name
        last_name = student.last_name
        username = (first_name[:min(3, len(first_name))].strip() + last_name[:min(4, len(last_name))].strip()).lower()
        student.username = username
        counter = 1
        while User.objects.filter(username=username):
            username = first_name + str(counter)
            counter += 1
        student.save()
        password = User.objects.make_random_password()
        student.set_password(password)
        student.save()
        your_stage = Your_Stage()
        your_stage.user = student
        your_stage.role = 'STUDENT'
        your_stage.stage = stage
        your_stage.save()
        student.your_stage = your_stage
        student.save()
        Initial_Password.objects.create(student=student, password=password)
        return redirect('/your_classes')
    context = {'stage': stage, 'form': form}
    template_name = 'add_student.html'
    return render(request, template_name, context)

@staff_member_required
def delete_class(request, pk):
    stage = get_object_or_404(Stage, pk=pk, teacher=request.user)
    if request.method == "POST":
        stage.delete()
        return redirect('/your_classes')
    template_name = 'delete_class.html'
    context = {'stage': stage}
    return render(request, template_name, context)

@staff_member_required
def add_class(request):
    context = {}
    template_name = "add_class.html"
    if request.POST:
        stage_name  = request.POST['stage_name']
        size        = request.POST['size']
        new_stage   = Stage()
        new_stage.title     = stage_name
        new_stage.teacher   = request.user
        new_stage.number    = size
        new_stage.save()
        pk = new_stage.pk
        return redirect(f"/your_classes/add/next/{new_stage.pk}")
    return render(request, template_name, context)

@staff_member_required
def add_class_next(request, pk):
    stage       = Stage.objects.get(pk=pk)
    students    = Your_Stage.objects.filter(stage=stage)
    if students:
        return redirect('/') 
    else:
        range_ = range(stage.number)
        context = {'size': stage.number, 'name': stage.title, 'range_': range_}
        template_name = 'add_class_next.html'
        if request.POST:
            passwords = {}
            for idx in range_:
                first_name = request.POST[str(idx)+'.first_name'].strip()
                last_name = request.POST[str(idx)+'.last_name'].strip()
                username = (first_name[:min(3, len(first_name))].strip() + last_name[:min(4, len(last_name))].strip()).lower()
                counter = 1
                while User.objects.filter(username=username):
                    username = first_name + str(counter)
                    counter += 1
                student = User.objects.create_user(username=username, first_name=first_name, last_name=last_name)
                student.save()
                password = User.objects.make_random_password()
                student.set_password(password)
                student.save()
                passwords[student] = password
                your_stage = Your_Stage()
                your_stage.user = student
                your_stage.role = 'STUDENT'
                your_stage.stage = stage
                your_stage.save()
                student.your_stage = your_stage
                student.save()
                Initial_Password.objects.create(student=student, password=password)
            stage.passwords = passwords
            # print(stage, stage.passwords)
            return add_class_next_next(request, passwords)
            # return redirect('/')
        return render(request, template_name, context)
    
@staff_member_required
def add_class_next_next(request, passwords):
    template_name = "add_class_next_next.html"
    context = {'passwords': passwords}
    return render(request, template_name, context)