# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ModuleStat'
        db.create_table('bigbrother_modulestat', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modulename', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('bigbrother', ['ModuleStat'])


    def backwards(self, orm):
        
        # Deleting model 'ModuleStat'
        db.delete_table('bigbrother_modulestat')


    models = {
        'bigbrother.modulestat': {
            'Meta': {'object_name': 'ModuleStat'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modulename': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['bigbrother']
