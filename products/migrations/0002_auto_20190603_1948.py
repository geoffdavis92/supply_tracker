# Generated by Django 2.2.1 on 2019-06-04 00:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(limit_choices_to={'foo': {'bar': 'baz'}}, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Category'),
        ),
    ]
