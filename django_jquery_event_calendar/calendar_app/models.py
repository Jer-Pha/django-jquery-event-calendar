from django.contrib.auth.models import User
from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    day = models.IntegerField()
    notes = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(User, related_name='events', on_delete=models.CASCADE, verbose_name='Creator')
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'time']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return f'{self.title} ({self.date})'