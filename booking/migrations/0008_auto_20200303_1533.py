# Generated by Django 3.0.3 on 2020-03-03 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_auto_20200303_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='min_name',
            field=models.CharField(default='none', max_length=20),
        ),
    ]
