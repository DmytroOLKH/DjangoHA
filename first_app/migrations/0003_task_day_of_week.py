# Generated by Django 5.2 on 2025-04-19 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0002_alter_category_options_alter_subtask_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='day_of_week',
            field=models.CharField(default='Monday', max_length=20),
            preserve_default=False,
        ),
    ]
