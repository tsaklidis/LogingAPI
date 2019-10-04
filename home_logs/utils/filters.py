# -*- coding: utf-8 -*-
from django.db.models import Q


def apply_filters(filters_dict, filter_fields, order, queryset):

    if not filter_fields:
        return queryset

    qset = Q()
    for key, value in filters_dict.iteritems():
        if key in filter_fields:
            qset &= Q(**{key: value})

    if order:
        return queryset.filter(qset).order_by(order).distinct()
    else:
        return queryset.filter(qset).distinct()
