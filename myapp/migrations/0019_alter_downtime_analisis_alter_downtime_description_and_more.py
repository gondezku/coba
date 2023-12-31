# Generated by Django 4.0.8 on 2023-10-05 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_downtime_analisis_downtime_spare_part'),
    ]

    operations = [
        migrations.AlterField(
            model_name='downtime',
            name='analisis',
            field=models.TextField(blank=True, default='', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='downtime',
            name='description',
            field=models.TextField(blank=True, default='', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='downtime',
            name='site_name',
            field=models.TextField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='downtime',
            name='site_section',
            field=models.PositiveSmallIntegerField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='downtime',
            name='site_sub_name',
            field=models.TextField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='downtime',
            name='spare_part',
            field=models.TextField(blank=True, default='', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='downtime',
            name='ticket_id',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='downtime',
            name='user_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
