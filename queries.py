import os
import django

from datetime import timedelta
from django.utils.timezone import now

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_proj.settings')
django.setup()

from first_app.models import Task, SubTask


# Создание записей:
# Task:
# title: "Prepare presentation".
# description: "Prepare materials and slides for the presentation".
# status: "New".
# deadline: Today's date + 3 days.

task1 = Task.objects.create(
    title="Prepare presentation",
    description="Prepare materials and slides for the presentation",
    status="New",
    deadline=now() + timedelta(days=3)
)

# SubTasks для "Prepare presentation":
# title: "Gather information".
# description: "Find necessary information for the presentation".
# status: "New".
# deadline: Today's date + 2 days.

subtask1 = SubTask.objects.create(
    task=task1,
    title="Gather information",
    description="Find necessary information for the presentation",
    status="New",
    deadline=now() + timedelta(days=2)
)

subtask2 = SubTask.objects.create(
    task=task1,
    title="Create slides",
    description="Create presentation slides",
    status="New",
    deadline=now() + timedelta(days=1)
)

print("Task and SubTasks created successfully!")

# Чтение записей:
# Tasks со статусом "New":
# Вывести все задачи, у которых статус "New".

tasks_new = Task.objects.filter(status="New")
for task in tasks_new:
    print(f"Title: {task.title}, Description: {task.description}, Deadline: {task.deadline}")

# SubTasks с просроченным статусом "Done":
# Вывести все подзадачи, у которых статус "Done", но срок выполнения истек.

subtasks_done_overdue = SubTask.objects.filter(status="Done", deadline__lt=now())
for subtask in subtasks_done_overdue:
    print(f"Title: {subtask.title}, Description: {subtask.description}, Deadline: {subtask.deadline}")

# Изменение записей:
# Измените статус "Prepare presentation" на "In progress".
# Измените срок выполнения для "Gather information" на два дня назад.
# Измените описание для "Create slides" на "Create and format presentation slides".

from first_app.models import Task

task = Task.objects.get(title="Prepare presentation")
task.status = "In progress"
task.save()
print(f"Task '{task.title}' status updated to '{task.status}'")

subtask = SubTask.objects.get(title="Gather information")
subtask.deadline = now() - timedelta(days=2)
subtask.save()
print(f"SubTask '{subtask.title}' deadline updated to '{subtask.deadline}'")

subtask = SubTask.objects.get(title="Create slides")
subtask.description = "Create and format presentation slides"
subtask.save()
print(f"SubTask '{subtask.title}' description updated to: {subtask.description}")

#Удалите задачу "Prepare presentation" и все ее подзадачи.

task = Task.objects.get(title="Prepare presentation")
task.subtasks.all().delete()
task.delete()
print("Task 'Prepare presentation' and its SubTasks have been deleted successfully!")