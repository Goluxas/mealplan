# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Arsenal'
        db.create_table('meals_arsenal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('meals', ['Arsenal'])

        # Adding model 'Entree'
        db.create_table('meals_entree', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('arsenal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meals.Arsenal'])),
        ))
        db.send_create_signal('meals', ['Entree'])


    def backwards(self, orm):
        # Deleting model 'Arsenal'
        db.delete_table('meals_arsenal')

        # Deleting model 'Entree'
        db.delete_table('meals_entree')


    models = {
        'meals.arsenal': {
            'Meta': {'object_name': 'Arsenal'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'meals.entree': {
            'Meta': {'object_name': 'Entree'},
            'arsenal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meals.Arsenal']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['meals']