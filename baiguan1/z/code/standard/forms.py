# -*- coding: utf-8 -*-

from django import forms
from django.db.models import Count, Q
from django.utils.translation import ugettext as _
from django.contrib.admin.helpers import ActionForm
from django.core.exceptions import ValidationError
from django.db import connection

from .models import *
import preprocessing
import collections

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'level', 'parent')

class StandardVendorForm(forms.ModelForm):
    class Meta:
        model = StandardVendor
        fields = ('status', 'name', 'standard_name')
        widgets = {
            'status': forms.RadioSelect(),
        }

class StandardSeriesForm(forms.ModelForm):
    class Meta:
        model = StandardSeries
        fields = ('status', 'vendor_short_name', 'brand', 'series', 'category')
        widgets = {
            'status': forms.RadioSelect(),
        }

class StandardCompanyForm(forms.ModelForm):
    class Meta:
        model = StandardCompany
        fields = ('keywords', )
        widgets = {
            'keywords': forms.Textarea(attrs = {'cols': 80, 'style': 'font: 13px/25px Arial;'}),
        }

    def clean_keywords(self):
        clean_keywords = self.cleaned_data['keywords']
        cursor = connection.cursor()
        out = collections.OrderedDict()
        for k in clean_keywords:
            c = k.strip()
            if StandardCompany.objects.exclude(id=self.instance.id).filter(keywords__contains=[c]).exists():
                  raise ValidationError(u'关键词 %s 已经存在' % c)
            out[c]=1
        return out.keys()


class StandardItemForm(forms.ModelForm):
    class Meta:
        model = StandardItem
        fields = ('status', 'name', 'model', 'flavor', 'series')
        widgets = {
            'status': forms.RadioSelect(),
            'flavor': forms.TextInput(attrs = {'class': 'prompt'}),
            'model': forms.TextInput(attrs = {'class': 'prompt'}),
        }

    # def save(self, force_insert=False, force_update=False, commit=True):
    #     m = super(StandardItemForm, self).save(commit=False)
    #     p_item = preprocessing.models.Item(m.name)
    #     m.keywords = p_item.keywords
    #     if commit:
    #         m.save()
    #     return m

class ExtractItemMetaForm(forms.Form):
    item_name = forms.CharField(label=u'商品名', max_length=255, widget=forms.TextInput(attrs={'value': u'$$美汁源果粒奶优芒果味水果牛奶饮料450g'}))

class SearchForm(forms.Form):
    q = forms.CharField(label=u'keywords', max_length=10000)


class ReviewStandardItemForm(forms.ModelForm):
    class Meta:
        model = StandardItem
        fields = ('name', 'series', 'model', 'flavor')
        widgets = {
            'flavor': forms.TextInput(attrs = {'class': 'prompt'}),
            'model': forms.TextInput(attrs = {'class': 'prompt'}),
        }

    def save(self, force_insert=False, force_update=False, commit=True):
        m = super(ReviewStandardItemForm, self).save(commit=False)
        p_item = preprocessing.models.Item(m.name)
        m.keywords = p_item.keywords
        m.status = 'human_verified'
        if commit:
            m.save()
        return m

class StandardItemBatchUpdateForm(forms.Form):
    brand = forms.CharField(required=False, label = u'品牌: ')
    series = forms.CharField(required=False, label = u'系列: ')
    category_id = forms.CharField(required=False)

class StandardVendorUpdateActionForm(ActionForm):
    standard_name = forms.CharField(required=False, label = u'企业名: ')

class StandardSeriesBatchUpdateForm(forms.Form):
    category_id = forms.CharField(required=False)


class StandardTagForm(forms.ModelForm):
    class Meta:
        model = StandardTag
        fields = ('tag', 'type')

    def clean_tag(self):
        out_tag = self.cleaned_data['tag'].upper()
        count = StandardTag.objects.filter(tag=out_tag).count()
        if count > 0:
            raise ValidationError(u'Tag already exists')
        return out_tag
