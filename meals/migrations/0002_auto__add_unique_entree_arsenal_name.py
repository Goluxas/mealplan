# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Entree', fields ['arsenal', 'name']
        db.create_unique('meals_entree', ['arsenal_id', 'name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Entree', fields ['arsenal', 'name']
        db.delete_unique('meals_entree', ['arsenal_id', 'name'])


    models = {
        'meals.arsenal': {
            'Meta': {'object_name': 'Arsenal'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'meals.entree': {
            'Meta': {'unique_together': "(('arsenal', 'name'),)", 'object_name': 'Entree'},
            'arsenal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meals.Arsenal']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['meals']