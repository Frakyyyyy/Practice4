from django.contrib import admin
from .models import Group, Student


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'surname', 'name', 'group', 'user', 'avatar')
    list_filter = ('group',)