# Generated by Django 4.0.3 on 2022-04-06 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('input', '0002_remove_planningsheet_assessment_phase_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SheetRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField(blank=True)),
                ('assessmentId', models.CharField(max_length=32)),
                ('student', models.CharField(max_length=64)),
                ('semester', models.CharField(max_length=16)),
                ('shortCode', models.CharField(max_length=16)),
                ('module', models.CharField(max_length=64)),
                ('grade', models.CharField(blank=True, max_length=16, null=True)),
                ('assessor', models.CharField(max_length=64)),
                ('assistant', models.CharField(blank=True, max_length=64, null=True)),
                ('startTime', models.DateTimeField(blank=True, null=True)),
                ('endTime', models.DateTimeField(blank=True, null=True)),
                ('assessmentStatus', models.CharField(blank=True, max_length=16, null=True)),
                ('assessmentStyle', models.CharField(max_length=16)),
                ('proposalText', models.TextField(blank=True, null=True)),
                ('assessmentType', models.CharField(max_length=16)),
                ('examinationForms', models.CharField(blank=True, max_length=16, null=True)),
                ('learningUnit', models.CharField(blank=True, max_length=64, null=True)),
                ('proposalStatus', models.CharField(blank=True, max_length=16, null=True)),
                ('createdAt', models.DateTimeField(blank=True, null=True)),
                ('updatedAt', models.DateTimeField(blank=True, null=True)),
                ('planning_sheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='input.planningsheet')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]