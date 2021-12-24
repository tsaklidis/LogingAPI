from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView

from home_logs.property.models import House, Space, Sensor
from home_logs.api.serializers import HouseSerializer
from home_logs.logs.models import Measurement
from home_logs.custom_auth.permissions import IsHouseOwner, IsSpaceOwner, \
    IsSpaceOwnerPack, IsAjax
from home_logs.utils.filters import apply_filters
from home_logs.api.serializers import *

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'limit'


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
    serializer_class = MeasurementSerializerRequest
    permission_classes = (IsAuthenticated, IsSpaceOwnerPack, )
    queryset = Measurement.objects.all()

    def post(self, request):
        pack = []
        for item in request.data:
            space_uuid = item.get('space_uuid', False)
            sensor_uuid = item.get('sensor_uuid', False)
            value = item.get('value', False)
            volt = item.get('volt', False)
            custom_created_on = item.get('custom_created_on', False)

            space = get_object_or_404(Space, uuid=space_uuid)
            try:
                sensor = space.sensors.get(uuid=sensor_uuid)
            except Sensor.DoesNotExist:
                info = {"detail": 'Sensor uuid not found'}
                return Response(info, status=status.HTTP_404_NOT_FOUND)

            measurement = {
                'space': space.pk,
                'sensor': sensor.pk,
                'value': value,
                'custom_created_on': custom_created_on
            }
            if volt:
                measurement['volt'] = volt

            pack.append(measurement)

        # Remove duplicates
        unique = [dict(t) for t in {tuple(d.items()) for d in pack}]

        serializer = self.serializer_class(data=unique, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        info = {
            "detail": "Package saved",
            "space": space.uuid,
            "sum": len(unique),
            'removed_duplicates': not(len(unique) == len(pack))
        }

        return Response(info, status=status.HTTP_201_CREATED)


class Measure(APIView):
    serializer_class = MeasurementSerializerRequest
    permission_classes = (IsAuthenticated, IsSpaceOwner, )
    queryset = Measurement.objects.all()

    def post(self, request):

        space_uuid = request.data.get('space_uuid', False)
        sensor_uuid = request.data.get('sensor_uuid', False)
        value = request.data.get('value', False)
        volt = request.data.get('volt', False)

        space = get_object_or_404(Space, uuid=space_uuid)
        sensor = get_object_or_404(Sensor, spaces=space, uuid=sensor_uuid)

        data = {'space': space.pk, 'sensor': sensor.pk, 'value': value}

        if volt:
            data['volt'] = volt

        serializer = self.serializer_class(data=data, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        info = {"detail": "Measurement saved", "space": space.uuid}

        return Response(info, status=status.HTTP_201_CREATED)


class MeasureList(ListAPIView):
    serializer_class = MeasurementSerializerPaginated
    permission_classes = (IsAuthenticated, IsSpaceOwner, IsAjax)
    queryset = Measurement.objects.all()
    pagination_class = PageNumberPagination

    def initial(self, request, *args, **kwargs):
        super(MeasureList, self).initial(request, **kwargs)
        space_uuid = request.GET.get('space_uuid')
        self.space = get_object_or_404(Space, uuid=space_uuid)
        self.check_object_permissions(request, self.space)

    def get(self, request, *args, **kwargs):
        sensor_uuid = request.GET.get('sensor_uuid')
        order_raw = request.GET.get('order_by')
        sensor = self.space.sensors.filter(spaces=self.space, uuid=sensor_uuid)

        filter_fields = (
            'created_on__date__year',
            'created_on__date__day', 'created_on__date__month',
            'created_on__date__day__lte', 'created_on__date__day__lt',
            'created_on__date__day__gte', 'created_on__date__day__gt',
            'created_on__date__month__lte', 'created_on__date__month__lt',
            'created_on__time__hour',
            'created_on__time__hour__lte', 'created_on__time__hour__lt',
            'created_on__time__hour__gte', 'created_on__time__hour__gt',
        )
        order_filters = ['created_on', '-created_on', 'value', '-value']

        if order_raw in order_filters:
            order = order_raw
        else:
            order = 'created_on'

        measurements = Measurement.objects.filter(space=self.space).order_by(order)

        filters_dict = {}
        for key, value in request.GET.items():
            if 'created_on__' + key in filter_fields:
                filters_dict['created_on__' + key] = value
        measurements = apply_filters(filters_dict, filter_fields, order, measurements)  # noqa

        if sensor:
            measurements = measurements.filter(sensor=sensor)

        paginator = CustomPagination()

        results = paginator.paginate_queryset(measurements, request)

        serializer = self.serializer_class(results, many=True)

        return paginator.get_paginated_response(serializer.data)


class MeasureListLast(MeasureList):
    serializer_class = MeasurementSerializer
    permission_classes = (IsAuthenticated, IsSpaceOwner, )
    pagination_class = None

    def get(self, request, *args, **kwargs):
        sensor_uuid = request.GET.get('sensor_uuid')

        if not sensor_uuid:
            return Response({'error':'Provide sensor_uuid'},
                            status=status.HTTP_400_BAD_REQUEST)

        sensor = self.space.sensors.filter(spaces=self.space, uuid=sensor_uuid)
        if not sensor:
            return Response({'error':'Bad sensor_uuid: {}'.format(sensor_uuid)},
                            status=status.HTTP_400_BAD_REQUEST)

        measurement = Measurement.objects.filter(space=self.space, sensor=sensor).last()
        serializer = self.serializer_class(measurement)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OpenMeasureList(MeasureList):
    permission_classes = (AllowAny,)

    def initial(self, request, *args, **kwargs):
        super(MeasureList, self).initial(request, **kwargs)
        self.space = get_object_or_404(Space, uuid='326f465d')


class OpenMeasureListLast(MeasureListLast):
    permission_classes = (AllowAny,)

    def initial(self, request, *args, **kwargs):
        super(MeasureList, self).initial(request, **kwargs)
        self.space = get_object_or_404(Space, uuid='326f465d')