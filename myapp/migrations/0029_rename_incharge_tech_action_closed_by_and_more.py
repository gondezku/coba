# Generated by Django 4.2.4 on 2023-10-09 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0028_tech_action_incharge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tech_action',
            old_name='incharge',
            new_name='closed_by',
        ),
        migrations.AddField(
            model_name='tech_action',
            name='taken_by',
            field=models.TextField(blank=True, max_length=50, null=True),
        ),
    ]
