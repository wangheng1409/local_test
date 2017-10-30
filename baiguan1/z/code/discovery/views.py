from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core import sql_utils
from .models import CollectionProduct
from datetime import datetime
import json

@login_required(login_url = '/login/')
def find_new_good(request, template = "discovery/products_list.html"):
    source = request.GET.get('source', 'tmall')
    area = request.GET.get('area', 'HB')
    order = request.GET.get('o', 'score')
    page = request.GET.get('page', 1)
    code = request.GET.get('code', 9)
    std_cat = request.GET.get('std_cat', '')
    grand = request.GET.get('grand', 'monthly')

    return render(request, template,{'mall': source,
                                     'page': page,
                                     'o': order,
                                     'code': code,
                                     'area': area,
                                     'std_cat': std_cat,
                                     'grand': grand
                                    })

def collect_commodity(request, template = "discovery/collected_list.html"):
    page = request.GET.get('page', 1)

    return render(request, template, {'page': page})

def product_info(request, template = "discovery/product_info.html"):
    tmall = settings.TMALL_ITEM_URL_PREFIX
    yhd = settings.YHD_ITEM_URL_PREFIX
    feiniu = settings.FEINIU_ITEM_URL_PREFIX
    skuid = request.GET.get('skuid', '')
    # grand = request.GET.get('grand', 'monthly')

    return render(request, template, {'tmall': tmall + skuid,
                                      'yhd': yhd + skuid,
                                      'feiniu': feiniu + skuid,
                                      'skuid': skuid,
                                      # 'grand': grand
                                      })

def products_category(request):
    sql = """
    SELECT
      parent_id,
      level,
      id,
      name
    FROM
      standard_category
      order by
      level
    """

    cur = connection.cursor()
    cur.execute(sql)
    result = sql_utils.dictfetchall(cur)

    return HttpResponse(json.dumps(result), content_type = 'application/json')

def product_collect(request):
    skuid = request.GET.get('skuid', '')
    name = request.GET.get('name', '')
    image = request.GET.get('image', '')
    source = request.GET.get('source', '')
    area = request.GET.get('area', '')
    exist = request.GET.get('exist', '')
    status = {'success': ''}
    product = CollectionProduct.objects.filter(user = request.user, product_id = skuid)
    if product.count() == 0:
        if exist == '':
            status['success'] = 1
        else:
            product = CollectionProduct.objects.get_or_create(user = request.user, product_id = skuid, product_name = name, product_image = image, product_source = source, product_area = area)
            status['success'] = 1
    else:
        if exist == '':
            status['success'] = 0
        else:
            CollectionProduct.objects.filter(user = request.user, product_id = skuid).delete()
            status['success'] = 0

    return HttpResponse(json.dumps(status), content_type = 'application/json')

def collected_product(request):
    products = CollectionProduct.objects.filter(user = request.user)
    paginator = Paginator(products, 30)

    page = request.GET.get('page', 1)
    try:
        items = paginator.page(page).object_list
    except PageNotAnInteger:
        items = paginator.page(1).object_list
    except EmptyPage:
        items = paginator.page(paginator.num_pages).object_list
    _products = list(items.values('product_id', 'collect_time', 'product_name', 'product_image', 'product_source', 'product_area'))
    for i in range(len(_products)):
        _products[i]['collect_time'] = _products[i]['collect_time'].strftime('%Y-%m-%d %H:%M:%S')

    out = {'result': _products,
           'page': page,
           'total': paginator.num_pages}

    return HttpResponse(json.dumps(out), content_type = 'application/json')

def product_list_collected(request):
    skuids = request.POST.getlist('skuids[0][]', [])
    source = request.POST.get('source')
    products = CollectionProduct.objects.filter(user = request.user, product_id__in = skuids, product_source = source)
    _products = list(products.values('product_id'))

    return HttpResponse(json.dumps({'result':_products}), content_type = 'application/json')

