"""
URL configuration for test_proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from first_app.views import django_greetings, guten_tag
from first_app.views import (
    TaskCreateView,
    TaskStatsView,
    TaskDetailView,
    CategoryCreateView,
    SubTaskCreateView,
    TaskListView,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView)



urlpatterns = [
    path('admin/', admin.site.urls),
    # path('greetings/', django_greetings),
    # path('hello/', guten_tag),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks_details/<int:task_id>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/stats/', TaskStatsView.as_view(), name='task-stats'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('subtasks/create/', SubTaskCreateView.as_view(), name='subtask-create'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:id>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),

             ]


