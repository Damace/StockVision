# Generated by Django 5.1.5 on 2025-02-09 03:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_product_supplier'),
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsale',
            name='product',
            field=models.ForeignKey(default=23, on_delete=django.db.models.deletion.CASCADE, to='inventory.product'),
            preserve_default=False,
        ),
    ]
