# Generated by Django 4.0.3 on 2022-04-30 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0004_module_alternative_length_module_standard_length'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='alternative_length',
        ),
        migrations.RemoveField(
            model_name='module',
            name='standard_length',
        ),
    ]
