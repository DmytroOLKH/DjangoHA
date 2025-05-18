from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from first_app.views import TaskListCreateView, TaskRetrieveUpdateDestroyView, SubTaskListCreateView, \
    SubTaskRetrieveUpdateDestroyView, TaskListView, RegisterView, LogoutView, ProfileView


schema_view = get_schema_view(
    openapi.Info(
        title="Task API",
        default_version="v1",
        description="Документация API",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/list_create/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-detail'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskRetrieveUpdateDestroyView.as_view(), name='subtask-detail'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-docs'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-docs'),
           ]






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
# from django.contrib import admin
# from django.urls import path
# from first_app.views import django_greetings, guten_tag
# from first_app.views import        (
#     CategoryCreateView,
#     TaskCreateView,
#     TaskStatsView,
#     TaskDetailView,
#     TaskListView,
#     FilteredSubtaskListView,
#     SubTaskCreateView,
#     SubTaskListView,
#     SubTaskListCreateView,
#     SubTaskDetailUpdateDeleteView   )
#
#
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # path('greetings/', django_greetings),
#     # path('hello/', guten_tag),
#     path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
#     path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
#     path('tasks/', TaskListView.as_view(), name='task-list'),
#     path('tasks_details/<int:task_id>/', TaskDetailView.as_view(), name='task-detail'),
#     path('tasks/stats/', TaskStatsView.as_view(), name='task-stats'),
#     path('subtasks/create/', SubTaskCreateView.as_view(), name='subtask-create'),
#     path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
#     path('subtasks/list_view', SubTaskListView.as_view(), name='subtask-list'),
#     path('subtasks/<int:id>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
#     path('filtered_subtasks/', FilteredSubtaskListView.as_view(), name='filtered-subtask-list'),
#     path('api/', include(router.urls)),
#     path('api-auth/', include('rest_framework.urls')),
#              ]
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
#     path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-detail'),
#     path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
#     path('subtasks/<int:pk>/', SubTaskRetrieveUpdateDestroyView.as_view(), name='subtask-detail'),
#     #path('', include(router.urls)),
#     ]


