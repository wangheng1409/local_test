# -*- coding: utf-8 -*-

from django import forms
from .models import *

# class DailyStoreItemSummaryForm(forms.ModelForm):
#     class Meta:
#         model = DailyStoreItemSummary
#         fields = ('date', 'store', 'item', 'sales', 'num', 'barcode', 'model', 'flavor', 'category_id')

# class DailyStoreSummaryForm(forms.ModelForm):
#     class Meta:
#         model = DailyStoreSummary
#         fields = ('date', 'store', 'sales', 'num', 'num_sku')

class QueryForm(forms.Form):
    q = forms.CharField(label=u'query', max_length=255)