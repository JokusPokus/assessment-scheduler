# Generated by Django 4.0.3 on 2022-04-30 16:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0003_module_organization_student_organization_exam'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='alternative_length',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(360)]),
        ),
        migrations.AddField(
            model_name='module',
            name='standard_length',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(360)]),
        ),
    ]
