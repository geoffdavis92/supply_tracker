from django.contrib import admin
from .models import Category, Product
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
  list_display = ("__str__", "group")
  search_fields = ("name", "group")

class ProductAdmin(admin.ModelAdmin):
  list_display = (Product.__str__, "date_purchased", "date_finished", "is_finished", "is_expired")
  search_fields = ("name",)
  # list_filter = ["category"]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)