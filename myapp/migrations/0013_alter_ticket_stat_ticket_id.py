# Generated by Django 4.2.4 on 2023-09-26 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_alter_ticket_stat_pe_approved_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket_stat',
            name='ticket_id',
            field=models.IntegerField(default=0),
        ),
    ]
