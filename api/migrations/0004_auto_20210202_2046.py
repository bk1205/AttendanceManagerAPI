# Generated by Django 3.1.4 on 2021-02-02 15:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210202_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='attendance_date',
            field=models.DateField(default=datetime.datetime(2021, 2, 2, 20, 46, 20, 598994)),
        ),
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together=set(),
        ),
    ]
