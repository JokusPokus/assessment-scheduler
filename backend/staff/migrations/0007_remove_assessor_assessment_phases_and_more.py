# Generated by Django 4.0.3 on 2022-05-03 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0006_assessor_windows_helper_windows'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assessor',
            name='assessment_phases',
        ),
        migrations.RemoveField(
            model_name='helper',
            name='assessment_phases',
        ),
    ]
