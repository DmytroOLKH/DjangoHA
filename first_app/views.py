
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from first_app.models import Task, SubTask
from first_app.serializers import TaskSerializer, SubTaskSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

class TaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class SubTaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

class SubTaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer

# from django.http import HttpResponse
# from django.db.models import Count
# from django.utils.timezone import now
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.pagination import PageNumberPagination
# from rest_framework import status
# from first_app.models import Task, Category, SubTask
# from first_app.serializers import (
#     TaskSerializer,
#     SubTaskSerializer,
#     SubTaskCreateSerializer,
#     CategoryCreateSerializer,
#     TaskDetailSerializer,
#     TaskCreateSerializer
# )

# def django_greetings(request) -> HttpResponse:
#     return HttpResponse("<h1>Greetings from the Django APP!!! :)</h1>")
#
# def guten_tag(request):
#     return HttpResponse("<h1>Guten Tag !, Herr Dmytr0 !<h1>")
#
# class TaskCreateView(APIView):
#     def post(self, request):
#         serializer = TaskCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class TaskDetailView(APIView):
#     def get(self, request, task_id, *args, **kwargs):
#         try:
#             task = Task.objects.get(id=task_id)
#             serializer = TaskDetailSerializer(task)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Task.DoesNotExist:
#             return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
#
# class TaskStatsView(APIView):
#     def get(self, request, *args, **kwargs):
#         total_tasks = Task.objects.count()
#         statuses = Task.objects.values('status').annotate(count=Count('status'))
#         overdue_tasks = Task.objects.filter(deadline__lt=now()).count()
#
#         stats = {
#             "total_tasks": total_tasks,
#             "tasks_by_status": {status['status']: status['count'] for status in statuses},
#             "overdue_tasks": overdue_tasks,
#         }
#         return Response(stats, status=status.HTTP_200_OK)
#
# class CategoryCreateView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = CategoryCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, id, *args, **kwargs):
#         try:
#             category = Category.objects.get(id=id)
#         except Category.DoesNotExist:
#             return Response({"error": "Категория не найдена"}, status=status.HTTP_404_NOT_FOUND)
#
#         serializer = CategoryCreateSerializer(category, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class SubTaskCreateView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = SubTaskCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class SubTaskListCreateView(APIView):
#     def get(self, request, *args, **kwargs):
#         subtasks = SubTask.objects.all()
#         serializer = SubTaskSerializer(subtasks, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request, *args, **kwargs):
#         serializer = SubTaskCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class SubTaskDetailUpdateDeleteView(APIView):
#     def get(self, request, id, *args, **kwargs):
#         try:
#             subtask = SubTask.objects.get(id=id)
#         except SubTask.DoesNotExist:
#             return Response({"error": "Подзадача не найдена"}, status=status.HTTP_404_NOT_FOUND)
#
#         serializer = SubTaskSerializer(subtask)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, id, *args, **kwargs):
#         try:
#             subtask = SubTask.objects.get(id=id)
#         except SubTask.DoesNotExist:
#             return Response({"error": "Подзадача не найдена"}, status=status.HTTP_404_NOT_FOUND)
#
#         serializer = SubTaskSerializer(subtask, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, id, *args, **kwargs):
#         try:
#             subtask = SubTask.objects.get(id=id)
#         except SubTask.DoesNotExist:
#             return Response({"error": "Подзадача не найдена"}, status=status.HTTP_404_NOT_FOUND)
#
#         subtask.delete()
#         return Response({"message": "Подзадача успешно удалена"}, status=status.HTTP_204_NO_CONTENT)
#
# class SubTaskPagination(PageNumberPagination):
#     page_size = 5
#
# class SubTaskListView(APIView):
#     def get(self, request):
#         queryset = SubTask.objects.all().order_by('-created_at')
#         paginator = SubTaskPagination()
#         page = paginator.paginate_queryset(queryset, request)
#         serializer = SubTaskSerializer(page, many=True)
#         return paginator.get_paginated_response(serializer.data)
#
# class TaskListView(APIView):
#     def get(self, request):
#         day_of_week = request.query_params.get('day', None)
#         if day_of_week:
#             tasks = Task.objects.filter(day_of_week__iexact=day_of_week)
#         else:
#             tasks = Task.objects.all()
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
# class FilteredSubtaskListView(APIView):
#     def get(self, request):
#         queryset = SubTask.objects.all().order_by('-created_at')
#
#         task_id = request.query_params.get('task')
#         if task_id:
#             queryset = queryset.filter(task_id=task_id)
#
#         status_param = request.query_params.get('status')
#         if status_param:
#             queryset = queryset.filter(status=status_param)
#
#         paginator = SubTaskPagination()
#         page = paginator.paginate_queryset(queryset, request)
#         serializer = SubTaskSerializer(page, many=True)
#         return paginator.get_paginated_response(serializer.data)
