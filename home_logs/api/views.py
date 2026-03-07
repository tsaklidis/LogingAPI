import datetime

from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView

from home_logs.property.models import House, Space, Sensor
from home_logs.logs.models import Measurement
from home_logs.custom_auth.permissions import IsHouseOwner, IsSpaceOwner, \
    IsSpaceOwnerPack, IsAjax
from home_logs.utils.filters import apply_filters
from home_logs.api.serializers import *  # noqa


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'limit'


class HouseAllList(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser, )
    serializer_class = HouseSerializer

    def get(self, request):
        houses = House.objects.prefetch_related(
            'spaces__sensors__kind'
        ).all()
        serializer = self.serializer_class(houses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HouseMyList(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = HouseSerializer

    def get(self, request):
        houses = House.objects.prefetch_related(
            'spaces__sensors__kind'
        ).filter(owner=request.user)
        serializer = self.serializer_class(houses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HouseSpecificList(APIView):
    permission_classes = (IsAuthenticated, IsHouseOwner, )
    serializer_class = HouseSerializer

    def get(self, request, uuid=None):
        house = get_object_or_404(
            House.objects.prefetch_related('spaces__sensors__kind'),
            uuid=uuid
        )
        serializer = self.serializer_class(house, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MeasurementPack(APIView):
    serializer_class = MeasurementSerializerRequest
    permission_classes = (IsAuthenticated, IsSpaceOwnerPack, )

    def post(self, request):
        # Collect all unique space/sensor UUIDs upfront
        space_uuids = set()
        sensor_uuids = set()
        for item in request.data:
            space_uuids.add(item.get('space_uuid'))
            sensor_uuids.add(item.get('sensor_uuid'))

        # Batch-fetch spaces and sensors in 2 queries instead of N
        spaces_qs = Space.objects.filter(
            uuid__in=space_uuids
        ).prefetch_related('sensors')
        spaces_by_uuid = {s.uuid: s for s in spaces_qs}

        sensors_qs = Sensor.objects.filter(uuid__in=sensor_uuids)
        sensors_by_uuid = {s.uuid: s for s in sensors_qs}

        pack = []
        last_space = None
        for item in request.data:
            space_uuid = item.get('space_uuid', False)
            sensor_uuid = item.get('sensor_uuid', False)
            value = item.get('value', False)
            volt = item.get('volt', False)
            custom_created_on = item.get('custom_created_on', False)

            space = spaces_by_uuid.get(space_uuid)
            if not space:
                return Response(
                    {"detail": "Space uuid not found: {}".format(space_uuid)},
                    status=status.HTTP_404_NOT_FOUND
                )

            sensor = sensors_by_uuid.get(sensor_uuid)
            if not sensor:
                return Response(
                    {"detail": "Sensor uuid not found: {}".format(sensor_uuid)},
                    status=status.HTTP_404_NOT_FOUND
                )

            measurement = {
                'space': space.pk,
                'sensor': sensor.pk,
                'value': value,
                'custom_created_on': custom_created_on
            }
            if volt:
                measurement['volt'] = volt

            pack.append(measurement)
            last_space = space

        # Remove duplicates
        unique = [dict(t) for t in {tuple(d.items()) for d in pack}]

        serializer = self.serializer_class(data=unique, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        info = {
            "detail": "Package saved",
            "space": last_space.uuid if last_space else None,
            "sum": len(unique),
            'removed_duplicates': len(unique) != len(pack)
        }

        return Response(info, status=status.HTTP_201_CREATED)


class Measure(APIView):
    serializer_class = MeasurementSerializerRequest
    permission_classes = (IsAuthenticated, IsSpaceOwner, )

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
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Measurement.objects.select_related(
            'sensor__kind'
        ).all()

    def initial(self, request, *args, **kwargs):
        super(MeasureList, self).initial(request, **kwargs)
        space_uuid = request.GET.get('space_uuid')
        self.space = get_object_or_404(Space, uuid=space_uuid)
        self.check_object_permissions(request, self.space)

    def get(self, request, *args, **kwargs):
        sensor_uuid = request.GET.get('sensor_uuid')
        order_raw = request.GET.get('order_by')
        latest_hours = request.GET.get('latest_hours')

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

        # Use select_related to avoid N+1 on sensor.kind
        measurements = self.get_queryset().filter(
            space=self.space
        ).order_by(order)

        if latest_hours:
            date_from = timezone.now() - datetime.timedelta(
                hours=int(latest_hours)
            )
            measurements = measurements.filter(created_on__gte=date_from)
        else:
            filters_dict = {}
            for key, value in request.GET.items():
                if 'created_on__' + key in filter_fields:
                    filters_dict['created_on__' + key] = value
            if filters_dict:
                measurements = apply_filters(
                    filters_dict, filter_fields, order, measurements
                )

        # Filter by sensor using a single object, not a queryset
        if sensor_uuid:
            sensor = self.space.sensors.filter(
                uuid=sensor_uuid
            ).first()
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
            return Response(
                {'error': 'Provide sensor_uuid'},
                status=status.HTTP_400_BAD_REQUEST
            )

        sensor = self.space.sensors.filter(uuid=sensor_uuid).first()
        if not sensor:
            return Response(
                {'error': 'Bad sensor_uuid: {}'.format(sensor_uuid)},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Use select_related and explicit ordering for .last()
        measurement = self.get_queryset().filter(
            space=self.space, sensor=sensor
        ).order_by('created_on').last()

        if not measurement:
            return Response(
                {'error': 'No measurements found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.serializer_class(measurement)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OpenMeasureList(MeasureList):
    permission_classes = (AllowAny,)

    def initial(self, request, *args, **kwargs):
        super(OpenMeasureList, self).initial(request, **kwargs)
        self.space = get_object_or_404(Space, uuid='326f465d')


class OpenMeasureListLast(MeasureListLast):
    permission_classes = (AllowAny,)

    def initial(self, request, *args, **kwargs):
        super(OpenMeasureListLast, self).initial(request, **kwargs)
        self.space = get_object_or_404(Space, uuid='326f465d')