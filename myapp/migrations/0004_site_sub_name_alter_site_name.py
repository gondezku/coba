# Generated by Django 4.2.4 on 2023-09-17 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_profile_is_lead_alter_profile_is_super_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='sub_name',
            field=models.TextField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='site',
            name='name',
            field=models.TextField(max_length=50),
        ),
    ]
