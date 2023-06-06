from django.contrib import admin

from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'date',
        'time',
        'day',
        'short_notes',
    )

    ordering = ('-date', '-time')
    empty_value_display = '-none-'

    @admin.display(description='Notes')
    def short_notes(self, obj):
        if len(obj.notes) > 32:
            return obj.notes[:30] + '..'
        else:
            return obj.notes