from django.contrib import admin

from home_logs.notifications.models import Notification, Alert


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    model = Alert
    list_display = ('title', 'space', 'sensor',
                    'value', 'min_value', 'max_value',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    model = Notification
    list_display = ('email', 'id',)
