# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'ModuleStat.value'
        db.alter_column('bigbrother_modulestat', 'value', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2))


    def backwards(self, orm):
        
        # Changing field 'ModuleStat.value'
        db.alter_column('bigbrother_modulestat', 'value', self.gf('django.db.models.fields.IntegerField')())


    models = {
        'bigbrother.modulestat': {
            'Meta': {'object_name': 'ModuleStat'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modulename': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        }
    }

    complete_apps = ['bigbrother']
