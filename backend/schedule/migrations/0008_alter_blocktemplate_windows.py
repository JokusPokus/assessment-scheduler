# Generated by Django 4.0.3 on 2022-03-30 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0007_examslot_alter_blocktemplate_windows_delete_slot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blocktemplate',
            name='windows',
            field=models.ManyToManyField(related_name='block_templates', to='schedule.window'),
        ),
    ]