# Generated by Django 4.0.8 on 2023-10-05 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_alter_downtime_analisis_alter_downtime_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='downtime',
            name='site_section',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='downtime',
            name='status',
            field=models.TextField(blank=True, default='', max_length=50, null=True),
        ),
    ]