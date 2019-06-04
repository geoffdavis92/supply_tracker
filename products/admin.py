from django.contrib import admin
from .models import Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
  list_display = (Product.__str__, "date_purchased", "date_finished", "is_finished")
  search_fields = ("name",)
  # list_filter = ["category"]

admin.site.register(Product, ProductAdmin)