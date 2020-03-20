from rest_framework import serializers
from rest_framework.fields import FloatField

from home_logs.property.models import House, Space, Sensor
from home_logs.logs.models import Measurement


class SensorSerializer(serializers.ModelSerializer):

    def to_representation(self, sensor):
        return {
            'uuid': sensor.uuid,
            'name': sensor.name,
            'kind': sensor.kind.name
        }

    class Meta:
        model = Sensor


class SpaceSerializer(serializers.ModelSerializer):

    sensors = SensorSerializer(read_only=True, many=True)

    class Meta:
        model = Space
        fields = ('name', 'uuid', 'square_meters', 'sensors', )


class HouseSerializer(serializers.ModelSerializer):

    spaces = SpaceSerializer(read_only=True, many=True)
    # username = serializers.CharField(source='owner.username')

    class Meta:
        model = House
        fields = ('name', 'uuid', 'spaces',)


class MeasurementSerializer(serializers.ModelSerializer):

    created = serializers.SerializerMethodField()
    value = FloatField()

    def get_created(self, ms):
        # query is based on created on with time diff
        return ms.created_localtime.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Measurement
        fields = ('created', 'value',)


class MeasurementSerializerPaginated(serializers.HyperlinkedModelSerializer):

    created_on = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    value = FloatField()

    def get_created_on(self, ms):
        return ms.created_localtime.strftime('%Y-%m-%d %H:%M:%S')

    def get_time(self, ms):
        return ms.created_localtime.strftime('%H:%M')

    class Meta:
        model = Measurement
        fields = ('value', 'created_on', 'time',)
