# Generated by Django 5.1.1 on 2024-09-21 08:12

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='revenue.project')),
            ],
            options={
                'unique_together': {('project', 'name')},
            },
        ),
        migrations.CreateModel(
            name='RevenueLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('revenue', models.DecimalField(decimal_places=2, max_digits=10)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='revenue_logs', to='revenue.task')),
            ],
            options={
                'unique_together': {('task', 'date')},
            },
        ),
    ]
