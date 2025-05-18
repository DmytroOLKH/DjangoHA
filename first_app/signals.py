from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Task

print("🔥 Сигналы загружены!")



@receiver(post_save, sender=Task)
def task_status_update(sender, instance, created, **kwargs):
    if not created:
        previous_status = Task.objects.get(pk=instance.pk).status  # Получаем предыдущий статус

        if previous_status == instance.status:
            print("🔹 Статус не изменился, уведомление НЕ отправляем.")
            return

        subject = f"Статус задачи изменен: {instance.title}"
        message = f"Ваша задача '{instance.title}' теперь в статусе '{instance.status}'."
        print(f"Email to: {instance.owner.email}\nSubject: {subject}\nMessage: {message}")