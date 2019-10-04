from django.core.exceptions import SuspiciousOperation
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination


from home_logs.property.models import House, Space, Sensor
from home_logs.api.serializers import HouseSerializer
from home_logs.logs.models import Measurement
from home_logs.custom_auth.permissions import IsHouseOwner, IsSpaceOwner, IsSpaceOwnerPack
from home_logs.utils.filters import apply_filters
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
    pagination_class = PageNumberPagination
    # queryset = Measurement.objects.all()

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
        # if not request.is_ajax():
        #     return Response(
        #         {'detail': 'Only ajax'},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        space_uuid = request.data.get('space_uuid', False)
        sensor_uuid = request.data.get('sensor_uuid', False)
        order_raw = request.GET.get('order_by', None)
        space = get_object_or_404(Space, uuid=space_uuid)
        sensor = space.sensors.filter(spaces=space, uuid=sensor_uuid)

        filter_fields = (
            'created_on__date__day', 'created_on__date__month',
            'created_on__date__day__lte', 'created_on__date__day__lt',
            'created_on__date__day__gte', 'created_on__date__day__gt',
            'created_on__date__month__lte', 'created_on__date__month__lt',
            'created_on__time__hour',
            'created_on__time__hour__lte', 'created_on__time__hour__lt',
            'created_on__time__hour__gte', 'created_on__time__hour__gt',
        )
        order_filters = ['created_on', '-created_on']

        if order_raw in order_filters:
            order = order_raw
        else:
            order = 'created_on'

        try:
            measurements = Measurement.objects.filter(
                space=space, sensor=sensor).order_by(order)
        except SuspiciousOperation:
            content = {'please move along': 'nothing to see here'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        filters_dict = {}
        for key, value in request.data.items():
            if 'created_on__' + key in filter_fields:
                filters_dict['created_on__' + key] = value
        measurements = apply_filters(filters_dict, filter_fields, order, measurements)  # noqa

        serializer = self.serializer_class(measurements, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
