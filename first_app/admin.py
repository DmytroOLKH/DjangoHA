from django.contrib import admin
from .models import Task, SubTask, Category

class SubTaskInline(admin.TabularInline):  #  TabularInline или StackedInline
    model = SubTask
    extra = 1  # Кол-во доп. пустых форм для подзадач

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['short_title', 'status', 'deadline', 'created_at']
    search_fields = ['title', 'description']
    list_filter = ['status', 'created_at']
    inlines = [SubTaskInline]

    def short_title(self, obj):
        if len(obj.title) > 10:
            return f"{obj.title[:10]}..."
        return obj.title

    short_title.short_description = "Название задачи (сокращённое)"


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'deadline', 'created_at', 'task']
    search_fields = ['title', 'description']
    list_filter = ['status', 'created_at']
    actions = ['mark_as_done']

    def mark_as_done(self, request, queryset):
        count = queryset.update(status="Done")
        self.message_user(request, f"{count} подзадач(и) успешно переведены в статус 'Done'.")

    mark_as_done.short_description = "Перевести выбранные подзадачи в статус Done"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']




