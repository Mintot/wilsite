# Generated by Django 3.0.3 on 2020-02-23 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='balance',
            field=models.IntegerField(default=0),
        ),
    ]
