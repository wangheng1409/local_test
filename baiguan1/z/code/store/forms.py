# -*- coding: utf-8 -*-

from django import forms
from django.db.models import Count, Q
from django.utils.translation import ugettext as _

from .models import *

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('name', 'parent_id', 'level')

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ('name', 'tags', 'customer_types', 'contact_name', 'contact_phone', 'bussiness_hours', 'store_scale', 'trading_area', 'trading_area', 'receipt_printing_freq')
        widgets = {
            'bussiness_hours': forms.RadioSelect(),
            'store_scale': forms.RadioSelect(),
            'receipt_printing_freq': forms.RadioSelect(),
        }

    def name_id_help_text(self, l):
        out = []
        for s in l:
            out.append('%s: %s' % (s[0], s[1]))
        return '<br>'.join(out)

    def __init__(self, *args, **kwargs):
        super(StoreForm, self).__init__(*args, **kwargs)
        self.fields['tags'].help_text = self.name_id_help_text(list(StoreTag.objects.values_list('name', 'id')))
        self.fields['customer_types'].help_text = self.name_id_help_text(list(CustomerType.objects.values_list('name', 'id')))


class StoreItemForm(forms.ModelForm):
    class Meta:
        model = StoreItem
        fields = ('status', 'store', 'name', 'receipt_item_id', 'price', 'trade_at', 'standard_item', 'image_url', 'image')
        widgets = {
            'status': forms.RadioSelect()
        }

class MatchForm(forms.Form):
    matched_id = forms.CharField(label=u'标品ID', max_length=255)

class SearchForm(forms.Form):
    q = forms.CharField(label=u'keywords', max_length=255)

class StoreIdsForm(forms.Form):
    store_ids = forms.CharField(label=u'Store IDs:', max_length=255)

class StoreDateRangePickerForm(forms.Form):
    start_date = forms.CharField(required=False)
    end_date = forms.CharField(required=False)
    store_id = forms.CharField()

class StoreDateRangePickerDetailForm(forms.Form):
    start_date = forms.CharField(required=False)
    end_date = forms.CharField(required=False)
    item_id = forms.CharField()

class StoreCategoryForm(forms.Form):
    start_date = forms.CharField(required=False)
    end_date = forms.CharField(required=False)
    store_id = forms.CharField()
    category = forms.CharField(required=False)

class StoreIdForm(forms.Form):
    store_id = forms.CharField()

class StoreShelfForm(forms.ModelForm):
    class Meta:
        model = StoreShelf
        fields = ('shelf_id', 'item_ids', 'layer', 'created_at')

class TransactionWechatAccountForm(forms.Form):
    mch_id = forms.CharField(required=True)
    appid = forms.CharField(required=True)
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    api_key = forms.CharField(required=True)

class TransactionAlipayAccountForm(forms.Form):
    appid = forms.CharField(required=True)
    pid = forms.CharField(required=True)
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    payment_password = forms.CharField(required=True)
    key = forms.CharField(required=True)          

class ThirdPartyDBInfoForm(forms.ModelForm):
    dbport = forms.CharField(required=False)
    dbname = forms.CharField(required=False)

    def __init__(self, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ThirdPartyDBInfoForm, self).__init__(**kwargs)

    def save(self, commit=True):
        obj = super(ThirdPartyDBInfoForm, self).save(commit=False)
        obj.user = self.request.user
        if commit:
            obj.save()
        return obj

    class Meta:
        model = ThirdPartyDBInfo
        fields = ('dbtype',
                  'dbname',
                  'dbhost',
                  'dbuser',
                  'dbpassword',
                  'dbport')
