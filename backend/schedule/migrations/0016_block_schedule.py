# Generated by Django 4.0.3 on 2022-05-25 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0015_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='schedule',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='blocks', to='schedule.schedule'),
            preserve_default=False,
        ),
    ]
