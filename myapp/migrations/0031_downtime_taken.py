# Generated by Django 4.2.4 on 2023-10-09 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0030_tech_action_action_taken_tech_action_sparepart'),
    ]

    operations = [
        migrations.AddField(
            model_name='downtime',
            name='taken',
            field=models.BooleanField(default=False),
        ),
    ]
