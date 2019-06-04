from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name="products_index"),
  path('categories', views.category_index, name="category_list"),
  path('category/<str:category_url>/', views.category_list, name="products_in_category")
] 