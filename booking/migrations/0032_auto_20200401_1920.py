# Generated by Django 3.0.3 on 2020-04-01 11:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0031_auto_20200401_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='book_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 1, 19, 20, 22, 747109)),
        ),
        migrations.AlterField(
            model_name='review',
            name='submit_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 1, 19, 20, 22, 747109)),
        ),
    ]
