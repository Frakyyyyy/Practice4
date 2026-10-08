from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('students/', views.student_list, name='list'),
    path('students/<int:student_id>/avatar/', views.edit_avatar, name='edit_avatar'),
]