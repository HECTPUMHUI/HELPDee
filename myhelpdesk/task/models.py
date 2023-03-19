from django.conf import settings
from django.db import models
from django.urls import reverse


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=True)
    status = models.ForeignKey('Status', on_delete=models.PROTECT, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-time_created']


class Status(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('status', kwargs={'status_id': self.pk})
