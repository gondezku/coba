# Generated by Django 4.2.4 on 2023-10-08 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0025_alter_downtime_kyt_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='downtime',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
