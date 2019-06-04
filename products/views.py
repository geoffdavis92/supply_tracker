from django.shortcuts import render
from .models import Product

# Create your views here.
def index(request):
  return render(request, 'products/index.liquid')

def category_index(request):
  category_list = []
  for category_group_key, category_group_tuple in Product.product_category_choices:
      for category_key, category_value in category_group_tuple:
        category_list.append((category_key,category_value,category_value.replace(' ','-')))
  return render(request, 'products/category_index.liquid', {
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
  return render(request, 'products/category_list.liquid', { 
    "category_key": category_key,
    "category_value": category_value,
    "products_in_category": products_in_category
  })