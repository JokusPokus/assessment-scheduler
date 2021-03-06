# Generated by Django 4.0.3 on 2022-03-30 10:45

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_slot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='block',
            name='exam_length',
        ),
        migrations.CreateModel(
            name='BlockTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField(blank=True)),
                ('block_length', models.IntegerField(validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(420)])),
                ('exam_length', models.IntegerField(validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(360)])),
                ('exam_start_times', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(), size=None)),
                ('windows', models.ManyToManyField(to='schedule.window')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
