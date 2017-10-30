# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

# from .forms import *
from .models import *

class CustomItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'barcode', 'name', 'model', 'flavor', 'series', 'category')
    search_fields = ('barcode' 'name', )
    list_filter = ('created_at', )

class MonitorBarcodesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',  'user', 'start_date', 'last_updated', 'created_at')
    raw_id_fields = ('user', )
    search_fields = ('user__first_name', )

admin.site.register(CustomItem, CustomItemAdmin)
admin.site.register(MonitorBarcodes, MonitorBarcodesAdmin)