# Generated by Django 5.2 on 2025-04-07 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category'},
        ),
        migrations.AlterModelOptions(
            name='subtask',
            options={'ordering': ['-created_at'], 'verbose_name': 'SubTask'},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['-created_at'], 'verbose_name': 'Task'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='subtask',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterModelTable(
            name='category',
            table='task_manager_category',
        ),
        migrations.AlterModelTable(
            name='subtask',
            table='task_manager_subtask',
        ),
        migrations.AlterModelTable(
            name='task',
            table='task_manager_task',
        ),
    ]
