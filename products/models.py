import datetime
from django.db import models
from django.core.validators import MinLengthValidator as min_len_val, MaxLengthValidator as max_len_val, MinValueValidator as min_value_val, MaxValueValidator as max_value_val
from django.utils import timezone
# Create your models here.

class Category(models.Model):
  CLEANING = "Cleaning"
  DRINK = "Drink"
  FOOD = "Food"
  TOILETRIES = "Toiletries"
  name = models.CharField(max_length=250, primary_key=True)
  category_group = models.CharField(max_length=250, choices=((CLEANING.upper(),CLEANING), (DRINK.upper(),DRINK), (FOOD.upper(),FOOD), (TOILETRIES.upper(),TOILETRIES)))
  def __str__(self):
    return self.name

class Product(models.Model):
  product_unit_choices = (
    ("box", "box"),
    ("bottle", "bottle"),
    ("case", "case"),
    ("dozen", "dozen"), 
    ("gallon", "gallon"),
    ("halfdozen", "half-dozen"),
    ("halfgallon", "half-gallon"), 
    ("roll", "roll"),
    ("sixpack", "six pack"),
  )
  product_category_choices = (
    ("Cleaning", (
      ("c_bath", "bathroom"),
      ("c_kitchen", "kitchen"),
      ("c_laundry", "laundry"),
      ("c_surfaces", "surface"),
      ("c_other", "other cleaner"),
    )),
    ("Drink", (
      ("d_beer", "beer"),
      ("d_dairy", "dairy"),
      ("d_juice", "juice"),
      ("d_liquer", "liquer"),
      ("d_liquor", "liquor"),
      ("d_pop", "soda pop"),
      ("d_soft", "soft drink"),
      ("d_other", "other drink"),
    )),
    ("Food", (
      ("f_cereal", "cereal"),
      ("f_condiment", "condiment"),
      ("f_fish", "fish"),
      ("f_meat", "meat"),
      ("f_snack", "snack"),
      ("f_spice", "spice"),
      ("f_other", "other food"),
    )),
    ("Toiletries", (
      ("t_bandages", "bandages"),
      ("t_bodywash", "body wash"),
      ("t_dental", "dental"),
      ("t_hairstyle", "hair styling"),
      ("t_hairwash", "hair wash"),
      ("t_medicine", "medicine"),
      ("t_tissue", "tissues"),
      ("t_other", "other toiletry"),
    )),
  )
  name = models.CharField(max_length=250, null=False, blank=False)
  price = models.DecimalField(default=0.00, max_digits=6, decimal_places=2, validators=[min_value_val(0.00),max_value_val(1_000.00)])
  quantity = models.IntegerField(default=1)
  unit = models.CharField(max_length=500, choices=product_unit_choices)
  category = models.CharField(blank=True,max_length=500, choices=product_category_choices) # models.ForeignKey('Category',null=True,on_delete=models.CASCADE)#
  date_purchased = models.DateField()
  date_expires = models.DateField(null=True, blank=True,)
  date_finished = models.DateField(null=True, blank=True,)
  date_delta = models.IntegerField(help_text="Difference in days between purchase and usage/expiration", null=True, blank=True, validators=[min_value_val(0)])
  is_finished = models.BooleanField(default=False)
  is_expired = models.BooleanField(default=False)

  def __str__(self):
    product_name = self.name.capitalize()
    return f"{product_name} ({self.quantity} {self.unit_choices_lookup(self.unit)})"
    
  # def category_choices_lookup(self, key_lookup):
  #   for category_group_key, category_group_tuple in self.product_category_choices:
  #     for category_key, category_value in category_group_tuple:
  #       if (key_lookup == category_key):
  #         return category_value
  #   return False

  def unit_choices_lookup(self, key_lookup):
    for unit_key, unit_value in self.product_unit_choices:
      if (key_lookup == unit_key): 
        return unit_value
    return False
  
  def get_date_delta(self):
    return (self.date_finished - self.date_purchased).days

  def finish(self):
    self.date_finished = timezone.now().date()
    self.date_delta = self.get_date_delta()
    self.is_finished = True
  
  def expire(self):
    self.finish()
    self.is_expired = True