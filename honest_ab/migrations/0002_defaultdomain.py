# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models


class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        orm.ExperimentDomain.objects.create(
            name="Default group",
            slug="default",
            active=True
        )

    def backwards(self, orm):
        "Write your backwards methods here."
        raise RuntimeError("Cannot reverse this migration")

    models = {
        u'honest_ab.experiment': {
            'Meta': {'object_name': 'Experiment'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'decision_class': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['honest_ab.ExperimentDomain']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'number_of_classes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2'}),
            'percentage_of_traffic': ('django.db.models.fields.FloatField', [], {'default': '100.0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'honest_ab.experimentallocation': {
            'Meta': {'unique_together': "(('model_pk', 'model', 'experiment'),)", 'object_name': 'ExperimentAllocation'},
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['honest_ab.Experiment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'model_pk': ('django.db.models.fields.BigIntegerField', [], {})
        },
        u'honest_ab.experimentdomain': {
            'Meta': {'object_name': 'ExperimentDomain'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'honest_ab.experimentdomainallocation': {
            'Meta': {'unique_together': "(('model_pk', 'model', 'experiment_domain'),)", 'object_name': 'ExperimentDomainAllocation'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'experiment_domain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['honest_ab.ExperimentDomain']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'model_pk': ('django.db.models.fields.BigIntegerField', [], {})
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
    symmetrical = True
