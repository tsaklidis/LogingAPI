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


class MeasurementSerializerRequest(serializers.ModelSerializer):
    value = FloatField()

    class Meta:
        model = Measurement
        fields = ('sensor', 'value', 'space')


class MeasurementSerializer(serializers.ModelSerializer):
    sensor = SensorSerializer()
    value = FloatField()

    class Meta:
        model = Measurement
        fields = ('sensor', 'value', 'created_on')


class Mea(serializers.ModelSerializer):

    class Meta:
        model = Measurement
        fields = ('sensor', 'value', 'created_on')


class MeasurementSerializerPaginated(serializers.HyperlinkedModelSerializer):
    sensor = SensorSerializer()
    value = FloatField()

    class Meta:
        model = Measurement
        fields = ('value', 'created_on', 'sensor', 'created_on')
