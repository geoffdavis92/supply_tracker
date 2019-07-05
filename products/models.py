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
  name = models.CharField(max_length=250,unique=True)
  group = models.CharField(max_length=250, choices=((CLEANING.upper(),CLEANING), (DRINK.upper(),DRINK), (FOOD.upper(),FOOD), (TOILETRIES.upper(),TOILETRIES)))

  def __str__(self):
    return f"{self.group} - {self.name}"

class Product(models.Model):
  product_unit_choices = (
    ("bag", "bag"),
    ("box", "box"),
    ("bottle", "bottle"),
    ("case", "case"),
    ("dozen", "dozen"), 
    ("gallon", "gallon"),
    ("halfdozen", "half-dozen"),
    ("halfgallon", "half-gallon"), 
    ("loaf", "loaf"),
    ("package", "package"),
    ("roll", "roll"),
    ("sixpack", "six pack"),
  )
  product_category_choices = (
    ("Cleaning", (
      "bathroom",
      "kitchen",
      "laundry",
      "surface",
      "other cleaner",
    )),
    ("Drink", (
      "beer",
      "dairy",
      "juice",
      "liquer",
      "liquor",
      "soda pop",
      "soft drink",
      "other drink",
    )),
    ("Food", (
      "cereal",
      "condiment",
      "fish",
      "meat",
      "snack",
      "spice",
      "other food",
    )),
    ("Toiletries", (
      "bandages",
      "body wash",
      "dental",
      "hair styling",
      "hair wash",
      "medicine",
      "tissues",
      "other toiletry",
    )),
  )
  name = models.CharField(max_length=250, null=False, blank=False)
  price = models.DecimalField(default=0.00, max_digits=6, decimal_places=2, validators=[min_value_val(0.00),max_value_val(1_000.00)])
  quantity = models.IntegerField(default=1)
  unit = models.CharField(max_length=500, choices=product_unit_choices)
  category = models.ForeignKey('Category',null=True,on_delete=models.CASCADE)
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
    if (not self.is_finished):
      self.date_finished = timezone.localtime(timezone.now()).date()
      self.date_delta = self.get_date_delta()
      self.is_finished = True
  
  def expire(self):
    self.finish()
    self.is_expired = True

# class Statistic(models.Model):
#   category = models.CharField(max_length=250, choices=Product)
#   categoryFK = models.ForeignKey('Category',null=True,on_delete=models.CASCADE)
