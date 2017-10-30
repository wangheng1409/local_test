# -*- coding: utf-8 -*-

from django import forms

class DateRangePickerForm(forms.Form):
    start_date = forms.CharField(required=False)
    end_date = forms.CharField(required=False)
    brand = forms.CharField()