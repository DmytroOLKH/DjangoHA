from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import views, generics, status
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from first_app.models import Task, SubTask, Category
from first_app.permissions import IsOwner
from first_app.serializers import TaskSerializer, SubTaskSerializer, CategorySerializer, RegisterSerializer


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response({"error": "Refresh token обязателен"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Выход выполнен, токен аннулирован"}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"error": "Невалидный или уже аннулированный токен"}, status=status.HTTP_400_BAD_REQUEST)


class TaskListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

class TaskListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated,IsOwner]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class SubTaskListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SubTaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer

class UserTasksView(ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)



class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Неверные данные'}, status=status.HTTP_401_UNAUTHORIZED)




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
