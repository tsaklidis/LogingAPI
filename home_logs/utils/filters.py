# -*- coding: utf-8 -*-
from django.db.models import Q


def apply_filters(filters_dict, filter_fields, order, queryset):

    if not filters_dict:
        return queryset

    qset = Q()
    for key, value in filters_dict.items():
        if key in filter_fields:
            qset &= Q(**{key: value})

    if order:
        return queryset.filter(qset).order_by(order)
    else:
        return queryset.filter(qset)
