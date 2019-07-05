from django.shortcuts import render
from .models import Product

# Create your views here.
def index(request):
  active_products = Product.objects.filter(is_finished=False, is_expired=False).order_by('date_expires','name')
  finished_products = Product.objects.filter(is_finished=True)
  expired_products = Product.objects.filter(is_expired=True)
  context = {
    "active_products": active_products,
    "finished_products": finished_products,
    "expired_products": expired_products
  }
  return render(request, 'products/index.html', context)

def product_detail(request, product_pk):
  product = Product.objects.get(pk=product_pk)
  return render(request,'products/detail.html', {
    "header_show_back": True,
    "product":product
  })

def category_index(request):
  category_list = []
  print(Product.product_category_choices)
  for category_group_key, category_group_tuple in Product.product_category_choices:
      for category_value in category_group_tuple:
        category_list.append((category_value,category_value.replace(' ','-')))
  return render(request, 'products/category_index.html', {
    "categories": category_list
  })

def category_list(request, category_url):
  for category_group_key, category_group_tuple in Product.product_category_choices:
    for c_key, c_value in category_group_tuple:
      if c_value == category_url.replace('-',' '):
        category_key = c_key
        category_value = c_value
  products_in_category = Product.objects.filter(category__contains=category_key)
  print({ 
    "category_key": category_key,
    "category_value": category_value,
    "category_url": category_url,
    "category_url_replaced": category_url.replace('-',' '),
    "products_in_category": products_in_category
  })
  return render(request, 'products/category_list.html', { 
    "category_key": category_key,
    "category_value": category_value,
    "products_in_category": products_in_category
  })