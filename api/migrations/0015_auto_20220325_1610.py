# Generated by Django 3.1.4 on 2022-03-25 10:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20220325_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='attendance_date',
            field=models.DateField(default=datetime.datetime(2022, 3, 25, 16, 10, 51, 946340)),
        ),
    ]
