from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from first_app.models import Task, Category, SubTask
from datetime import datetime


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

