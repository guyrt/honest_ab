# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, help_text=b'Set to false if the instance is deleted.')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128)),
                ('Experiment-specific salt', models.SlugField(unique=True, max_length=64)),
                ('percentage_of_traffic', models.FloatField(default=100.0, verbose_name='Percentage of eligible traffic to be assigned to this experiment.  Takes floating point value between 0 and 100')),
                ('buckets', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ExperimentDomain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, help_text=b'Set to false if the instance is deleted.')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text=b'Human readable name.', max_length=128)),
                ('slug', models.SlugField(help_text=b'Used as salt. Must be unique.', unique=True, max_length=64)),
                ('num_buckets', models.PositiveIntegerField(default=1000)),
                ('experimental_unit_resolver', models.CharField(default=b'honest_ab.unit_resolvers.cookie_resolver', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, help_text=b'Set to false if the instance is deleted.')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128)),
                ('slug', models.SlugField(unique=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='GoalAchieved',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('goal', models.ForeignKey(to='honest_ab.Goal')),
            ],
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('experiment', models.ForeignKey(to='honest_ab.Experiment')),
            ],
        ),
        migrations.AddField(
            model_name='experiment',
            name='domain',
            field=models.ForeignKey(to='honest_ab.ExperimentDomain'),
        ),
    ]
