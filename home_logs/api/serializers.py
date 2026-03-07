from rest_framework import serializers
from rest_framework.fields import FloatField, DateTimeField

from home_logs.property.models import House, Space, Sensor
from home_logs.logs.models import Measurement


class SensorSerializer(serializers.ModelSerializer):
    kind_name = serializers.CharField(source='kind.name', read_only=True)

    def to_representation(self, sensor):
        return {
            'uuid': sensor.uuid,
            'name': sensor.name,
            'kind': sensor.kind.name
        }

    class Meta:
        model = Sensor
        fields = ('uuid', 'name', 'kind_name',)

    @classmethod
    def setup_eager_loading(cls, queryset):
        return queryset.select_related('kind')


class SpaceSerializer(serializers.ModelSerializer):
    sensors = SensorSerializer(read_only=True, many=True)

    class Meta:
        model = Space
        fields = ('name', 'uuid', 'square_meters', 'sensors', )

    @classmethod
    def setup_eager_loading(cls, queryset):
        return queryset.prefetch_related('sensors__kind')


class HouseSerializer(serializers.ModelSerializer):
    spaces = SpaceSerializer(read_only=True, many=True)

    class Meta:
        model = House
        fields = ('name', 'uuid', 'spaces',)

    @classmethod
    def setup_eager_loading(cls, queryset):
        return queryset.prefetch_related('spaces__sensors__kind')


class MeasurementSerializerRequest(serializers.ModelSerializer):
    value = FloatField()

    class Meta:
        model = Measurement
        fields = ('sensor', 'value', 'space',)


class MeasurementSerializer(serializers.ModelSerializer):
    sensor = SensorSerializer()
    value = FloatField()

    class Meta:
        model = Measurement
        fields = ('sensor', 'value', 'created_on',)

    @classmethod
    def setup_eager_loading(cls, queryset):
        return queryset.select_related('sensor__kind')


class MeasurementSerializerPaginated(serializers.HyperlinkedModelSerializer):
    sensor = SensorSerializer()
    value = FloatField()

    class Meta:
        model = Measurement
        fields = ('value', 'created_on', 'sensor',)

    @classmethod
    def setup_eager_loading(cls, queryset):
        return queryset.select_related('sensor__kind')

