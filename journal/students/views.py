from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404

from .forms import StudentFilterForm, StudentAvatarForm
from .models import Student
def student_list(request):
    form = StudentFilterForm(request.GET or None)
    students = Student.objects.all()
    errors = []

    if request.GET:
        if form.is_valid():
            cleaned = form.cleaned_data
            surname_part = cleaned.get('surname_part')
            group = cleaned.get('group')
            group_name_part = cleaned.get('group_name_part')

            if surname_part:
                students = students.filter(surname__icontains=surname_part)
            if group:
                students = students.filter(group=group)
            if group_name_part:
                students = students.filter(group__name__icontains=group_name_part)
        else:
            errors = form.errors
            students = Student.objects.none()

    return render(request, 'students/student_list.html', {
        'form': form,
        'students': students,
        'errors': errors,
    })
    
@login_required
def edit_avatar(request, student_id):
    """Изменение аватара. Только свой собственный."""
    student = get_object_or_404(Student, pk=student_id)

    # Проверка: изменять может только сам студент
    if request.user != student.user:
        raise PermissionDenied('Вы можете изменять только свой аватар.')

    if request.method == 'POST':
        form = StudentAvatarForm(
            request.POST,
            request.FILES,
            instance=student,
        )
        if form.is_valid():
            form.save()
            return redirect('students:list')
    else:
        form = StudentAvatarForm(instance=student)

    return render(request, 'students/avatar_form.html', {
        'form': form,
        'student': student,
    })