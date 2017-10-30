# -*- coding: utf-8 -*-
import csv
from django.http import HttpResponse
from django.contrib.admin import utils

def export_queryset_as_csv(modeladmin, request, queryset):

    if hasattr(modeladmin, 'export_fields'):
        field_list = modeladmin.export_fields
    else:
        # Copy modeladmin.list_display to remove action_checkbox
        field_list = modeladmin.list_display[:]
        field_list.remove('action_checkbox')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="cm_data.csv"'

    writer = csv.writer(response)
    writer.writerow([
        utils.label_for_field(f, queryset.model, modeladmin).encode('utf-8') for f in field_list
    ])

    for obj in queryset:
        csv_line_values = []
        csv_line_tmp = []
        for field in field_list:
            field_obj, attr, value = utils.lookup_field(field, obj, modeladmin)
            if isinstance(value, unicode) :
                csv_line_values.append(value.encode('utf-8'))
            else:
                csv_line_values.append(value)
        writer.writerow(csv_line_values)

    return response
export_queryset_as_csv.short_description = u'导出CSV'