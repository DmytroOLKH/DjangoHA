from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from first_app.models import Task, Category, SubTask
from datetime import datetime
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]  # Проверка уникальности email
                                  )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')


    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают!")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

    def validate_name(self, value):
        model = self.Meta.model
        if self.instance:

            if value != self.instance.name and model.objects.filter(name=value).exists():
                raise ValidationError("Категория с таким названием уже существует.")
        else:

            if model.objects.filter(name=value).exists():
                raise ValidationError("Категория с таким названием уже существует.")
        return value

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubTaskCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    task = serializers.IntegerField()
    status = serializers.ChoiceField(choices=SubTask.STATUS_CHOICES, default='New')
    deadline = serializers.DateTimeField()

    def create(self, validated_data):
        task_id = validated_data.pop('task')
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            raise serializers.ValidationError({"task": "Task with this ID does not exist."})

        return SubTask.objects.create(task=task, **validated_data)

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'title': instance.title,
            'description': instance.description,
            'task': instance.task.id,
            'status': instance.status,
            'deadline': instance.deadline,
        }

class SubTaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = SubTask
        fields = '__all__'


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'subtasks']


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline']

    def validate_deadline(self, value):
        print("validate_deadline сработал:", value)
        if value.date() < datetime.now().date():
            raise serializers.ValidationError("Дата дедлайна не может быть в прошлом!")
        return value


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Task
        fields = '__all__'

