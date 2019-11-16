from rest_framework import serializers

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

    def to_representation(self, obj):
        return {
            # 'space': obj.space.uuid,
            # 'sensor': [{'uuid': obj.sensor.uuid, 'name': obj.sensor.name}],
            'value': obj.value,
            # query is based on created on with time diff
            'created_on': obj.created_localtime.strftime('%Y-%m-%d %H:%M:%S')
        }

    class Meta:
        model = Measurement
        fields = ('space', 'sensor', 'value', 'volt',
                  'created_on', 'created_localtime')


class MeasurementSerializerPaginated(serializers.HyperlinkedModelSerializer):

    def to_representation(self, obj):
        return {
            # 'space': obj.space.uuid,
            # 'sensor': [{'uuid': obj.sensor.uuid, 'name': obj.sensor.name}],
            'value': obj.value,
            # query is based on created on with time diff
            'created_on': obj.created_localtime.strftime('%Y-%m-%d %H:%M:%S'),
            'time': obj.created_localtime.strftime('%H:%M')
        }

    class Meta:
        model = Measurement
        fields = ('space', 'sensor', 'value',
                  'created_on', 'created_localtime')
