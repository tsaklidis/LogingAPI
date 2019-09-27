from django.contrib import admin

from home_logs.logs.models import Measurement


@admin.register(Measurement)
class MeasurementdAdmin(admin.ModelAdmin):
    model = Measurement
    list_display = ('space', 'sensor', 's_kind', 'value', 'created_on')

    def s_kind(self, ms):
        return ms.sensor.kind.name
    s_kind.short_description = 'Kind:'
