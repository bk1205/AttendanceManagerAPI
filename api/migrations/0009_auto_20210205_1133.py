# Generated by Django 3.1.4 on 2021-02-05 06:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20210204_2332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='attendance_date',
            field=models.DateField(default=datetime.datetime(2021, 2, 5, 11, 33, 27, 950014)),
        ),
    ]
