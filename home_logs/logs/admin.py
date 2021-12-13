from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from home_logs.logs.models import Measurement, DavisMeasurement


@admin.register(Measurement)
class MeasurementdAdmin(ImportExportModelAdmin):
    model = Measurement
    list_display = ('space', 'sensor', 's_kind', 'value', 'created_on')
    list_filter = ('space', 'sensor')

    def s_kind(self, ms):
        return ms.sensor.kind.name
    s_kind.short_description = 'Kind:'


@admin.register(DavisMeasurement)
class DavisMeasurementAdmin(ImportExportModelAdmin):
    model = DavisMeasurement
    list_display = ('value', 'kind', 'measured', 'created_on')
    list_filter = ('kind',)
