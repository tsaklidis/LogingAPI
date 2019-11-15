from django.contrib import admin

from home_logs.property.models import (
    House, Sensor, Space, SpaceKind, SensorKind)


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    model = House
    list_display = ('name', 'spaces_count', 'sensors_count', 'created_on', )


@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    model = Space
    list_display = ('name', 'uuid', 'house',
                    'sensors_count', 'kind', 'created_on',)


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    model = Sensor
    list_display = ('name', 'kind', 'uuid')


@admin.register(SpaceKind)
class SpaceKindAdmin(admin.ModelAdmin):
    model = SpaceKind
    list_display = ('name',)


@admin.register(SensorKind)
class SensorKindAdmin(admin.ModelAdmin):
    model = SensorKind
    list_display = ('name',)
