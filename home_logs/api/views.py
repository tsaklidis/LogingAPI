from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from home_logs.property.models import House, Space, Sensor
from home_logs.api.serializers import HouseSerializer
from home_logs.logs.models import Measurement
from home_logs.custom_auth.permissions import IsHouseOwner, IsSpaceOwner, IsSpaceOwnerPack
from home_logs.api.serializers import MeasurementSerializer


class HouseAllList(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser, )
    serializer_class = HouseSerializer
    queryset = House.objects.all()

    def get(self, request):

        houses = self.queryset.all()

        serializer = self.serializer_class(houses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HouseMyList(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = HouseSerializer
    queryset = House.objects.all()

    def get(self, request):

        houses = self.queryset.filter(owner=request.user)

        serializer = self.serializer_class(houses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HouseSpecificList(APIView):
    permission_classes = (IsAuthenticated, IsHouseOwner, )
    serializer_class = HouseSerializer
    queryset = House.objects.all()

    def get(self, request, uuid=None):

        house = House.objects.get(uuid=uuid)

        serializer = self.serializer_class(house, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MeasurementPack(APIView):
    serializer_class = MeasurementSerializer
    permission_classes = (IsAuthenticated, IsSpaceOwnerPack, )
    queryset = Measurement.objects.all()

    def post(self, request):
        pack = []
        for item in request.data:
            space_uuid = item.get('space_uuid', False)
            sensor_uuid = item.get('sensor_uuid', False)
            value = item.get('value', False)

            space = get_object_or_404(Space, uuid=space_uuid)
            try:
                sensor = space.sensors.get(uuid=sensor_uuid)
            except Sensor.DoesNotExist:
                info = {"detail": 'Sensor uuid not found'}
                return Response(info, status=status.HTTP_404_NOT_FOUND)

            measurement = {
                'space': space.pk,
                'sensor': sensor.pk,
                'value': value
            }
            pack.append(measurement)

        # Remove duplicates
        unique = [dict(t) for t in {tuple(d.items()) for d in pack}]

        serializer = self.serializer_class(data=unique, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        info = {
            "detail": "Measurement package saved",
            "sum": len(unique),
            'removed_duplicates': not(len(unique) == len(pack))
        }

        return Response(info, status=status.HTTP_201_CREATED)


class Measure(APIView):
    serializer_class = MeasurementSerializer
    permission_classes = (IsAuthenticated, IsSpaceOwner, )
    queryset = Measurement.objects.all()

    def post(self, request):

        space_uuid = request.data.get('space_uuid', False)
        sensor_uuid = request.data.get('sensor_uuid', False)
        value = request.data.get('value', False)

        space = get_object_or_404(Space, uuid=space_uuid)
        sensor = get_object_or_404(Sensor, spaces=space, uuid=sensor_uuid)

        data = {'space': space.pk, 'sensor': sensor.pk, 'value': value}

        serializer = self.serializer_class(data=data, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        info = {"detail": "Measurement saved"}

        return Response(info, status=status.HTTP_201_CREATED)

    def get(self, request):
        # TODO add filtering by created on
        space_uuid = request.data.get('space_uuid', False)
        sensor_uuid = request.data.get('sensor_uuid', False)
        space = get_object_or_404(Space, uuid=space_uuid)
        sensor = space.sensors.filter(spaces=space, uuid=sensor_uuid)

        measurements = Measurement.objects.filter(space=space, sensor=sensor)

        serializer = self.serializer_class(measurements, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)