# Generated by Django 4.0.3 on 2022-03-30 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_window_block_length_block'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField(blank=True)),
                ('start_time', models.DateTimeField()),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slots', to='schedule.block')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
