# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ExperimentLayer'
        db.create_table(u'honest_ab_experimentlayer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=64)),
        ))
        db.send_create_signal(u'honest_ab', ['ExperimentLayer'])

        # Adding model 'Experiment'
        db.create_table(u'honest_ab_experiment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=64)),
            ('number_of_classes', self.gf('django.db.models.fields.PositiveIntegerField')(default=2)),
            ('percentage_of_traffic', self.gf('django.db.models.fields.FloatField')(default=100.0)),
            ('decision_class', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('layer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['honest_ab.ExperimentLayer'])),
        ))
        db.send_create_signal(u'honest_ab', ['Experiment'])

        # Adding model 'ExperimentAllocation'
        db.create_table(u'honest_ab_experimentallocation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('experiment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['honest_ab.Experiment'])),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('model_pk', self.gf('django.db.models.fields.BigIntegerField')()),
            ('group', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal(u'honest_ab', ['ExperimentAllocation'])

        # Adding unique constraint on 'ExperimentAllocation', fields ['model_pk', 'model', 'experiment']
        db.create_unique(u'honest_ab_experimentallocation', ['model_pk', 'model', 'experiment_id'])

        # Adding model 'Goal'
        db.create_table(u'honest_ab_goal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=64)),
        ))
        db.send_create_signal(u'honest_ab', ['Goal'])

        # Adding model 'GoalAchieved'
        db.create_table(u'honest_ab_goalachieved', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('experiment_allocation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['honest_ab.ExperimentAllocation'])),
            ('goal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['honest_ab.Goal'])),
        ))
        db.send_create_signal(u'honest_ab', ['GoalAchieved'])


    def backwards(self, orm):
        # Removing unique constraint on 'ExperimentAllocation', fields ['model_pk', 'model', 'experiment']
        db.delete_unique(u'honest_ab_experimentallocation', ['model_pk', 'model', 'experiment_id'])

        # Deleting model 'ExperimentLayer'
        db.delete_table(u'honest_ab_experimentlayer')

        # Deleting model 'Experiment'
        db.delete_table(u'honest_ab_experiment')

        # Deleting model 'ExperimentAllocation'
        db.delete_table(u'honest_ab_experimentallocation')

        # Deleting model 'Goal'
        db.delete_table(u'honest_ab_goal')

        # Deleting model 'GoalAchieved'
        db.delete_table(u'honest_ab_goalachieved')


    models = {
        u'honest_ab.experiment': {
            'Meta': {'object_name': 'Experiment'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'decision_class': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'layer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['honest_ab.ExperimentLayer']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'number_of_classes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2'}),
            'percentage_of_traffic': ('django.db.models.fields.FloatField', [], {'default': '100.0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'honest_ab.experimentallocation': {
            'Meta': {'unique_together': "(('model_pk', 'model', 'experiment'),)", 'object_name': 'ExperimentAllocation'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['honest_ab.Experiment']"}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'model_pk': ('django.db.models.fields.BigIntegerField', [], {})
        },
        u'honest_ab.experimentlayer': {
            'Meta': {'object_name': 'ExperimentLayer'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'honest_ab.goal': {
            'Meta': {'object_name': 'Goal'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'honest_ab.goalachieved': {
            'Meta': {'object_name': 'GoalAchieved'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'experiment_allocation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['honest_ab.ExperimentAllocation']"}),
            'goal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['honest_ab.Goal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['honest_ab']