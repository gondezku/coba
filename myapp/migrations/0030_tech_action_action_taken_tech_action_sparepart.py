# Generated by Django 4.2.4 on 2023-10-09 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0029_rename_incharge_tech_action_closed_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tech_action',
            name='action_taken',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tech_action',
            name='sparepart',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]
