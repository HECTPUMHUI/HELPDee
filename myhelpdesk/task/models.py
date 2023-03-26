from django.conf import settings
from django.db import models
from django.urls import reverse


class Task(models.Model):
    PROCESS_CHOICES = (
        ('in_progress', 'In Progress'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('process of recovery', 'Process of Recovery'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    process = models.CharField(max_length=255, choices=PROCESS_CHOICES, default='in_progress')
    status = models.ForeignKey('Status', on_delete=models.PROTECT, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=True)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-time_created']


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=1000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Status(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('status', kwargs={'status_id': self.pk})


class RestoreTask(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Restored Task'
        verbose_name_plural = 'Restored Tasks'
