# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'InstitutionType'
        db.create_table('careprofessional_institutiontype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
        ))
        db.send_create_signal('careprofessional', ['InstitutionType'])

        # Adding model 'PostGraduate'
        db.create_table('careprofessional_postgraduate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
        ))
        db.send_create_signal('careprofessional', ['PostGraduate'])

        # Adding model 'AcademicResume'
        db.create_table('careprofessional_academicresume', (
            ('id', self.gf('gestorpsi.util.uuid_field.UuidField')(max_length=36, primary_key=True)),
            ('teachingInstitute', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('institutionType', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['careprofessional.InstitutionType'], unique=True, null=True)),
            ('course', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('initialDateGraduation', self.gf('django.db.models.fields.DateField')(null=True)),
            ('finalDateGraduation', self.gf('django.db.models.fields.DateField')(null=True)),
            ('lattesResume', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('postGraduate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['careprofessional.PostGraduate'], null=True)),
            ('initialDatePostGraduate', self.gf('django.db.models.fields.DateField')(null=True)),
            ('finalDatePostGraduate', self.gf('django.db.models.fields.DateField')(null=True)),
            ('area', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
        ))
        db.send_create_signal('careprofessional', ['AcademicResume'])

        # Adding model 'Profession'
        db.create_table('careprofessional_profession', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('symbol_desc', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('academic_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('careprofessional', ['Profession'])

        # Adding model 'ProfessionalProfile'
        db.create_table('careprofessional_professionalprofile', (
            ('id', self.gf('gestorpsi.util.uuid_field.UuidField')(max_length=36, primary_key=True)),
            ('academicResume', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['careprofessional.AcademicResume'], unique=True, null=True)),
            ('initialProfessionalActivities', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('profession', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['careprofessional.Profession'], unique=True, null=True)),
            ('services', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('availableTime', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
        ))
        db.send_create_signal('careprofessional', ['ProfessionalProfile'])

        # Adding M2M table for field agreement on 'ProfessionalProfile'
        db.create_table('careprofessional_professionalprofile_agreement', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('professionalprofile', models.ForeignKey(orm['careprofessional.professionalprofile'], null=False)),
            ('agreement', models.ForeignKey(orm['organization.agreement'], null=False))
        ))
        db.create_unique('careprofessional_professionalprofile_agreement', ['professionalprofile_id', 'agreement_id'])

        # Adding M2M table for field workplace on 'ProfessionalProfile'
        db.create_table('careprofessional_professionalprofile_workplace', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('professionalprofile', models.ForeignKey(orm['careprofessional.professionalprofile'], null=False)),
            ('place', models.ForeignKey(orm['place.place'], null=False))
        ))
        db.create_unique('careprofessional_professionalprofile_workplace', ['professionalprofile_id', 'place_id'])

        # Adding model 'LicenceBoard'
        db.create_table('careprofessional_licenceboard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
        ))
        db.send_create_signal('careprofessional', ['LicenceBoard'])

        # Adding model 'ProfessionalIdentification'
        db.create_table('careprofessional_professionalidentification', (
            ('id', self.gf('gestorpsi.util.uuid_field.UuidField')(max_length=36, primary_key=True)),
            ('profession', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['careprofessional.Profession'], null=True)),
            ('registerNumber', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
        ))
        db.send_create_signal('careprofessional', ['ProfessionalIdentification'])

        # Adding model 'StudentProfile'
        db.create_table('careprofessional_studentprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lecture_class', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['careprofessional.Profession'], null=True, blank=True)),
            ('period', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('class_duration', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('register_number', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('professional', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['careprofessional.CareProfessional'], unique=True)),
        ))
        db.send_create_signal('careprofessional', ['StudentProfile'])

        # Adding model 'Availability'
        db.create_table('careprofessional_availability', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('hour', self.gf('django.db.models.fields.TimeField')()),
        ))
        db.send_create_signal('careprofessional', ['Availability'])

        # Adding model 'CareProfessional'
        db.create_table('careprofessional_careprofessional', (
            ('id', self.gf('gestorpsi.util.uuid_field.UuidField')(max_length=36, primary_key=True)),
            ('professionalIdentification', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['careprofessional.ProfessionalIdentification'], unique=True, null=True)),
            ('professionalProfile', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['careprofessional.ProfessionalProfile'], unique=True, null=True)),
            ('person', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['person.Person'], unique=True)),
            ('comments', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('careprofessional', ['CareProfessional'])

        # Adding M2M table for field availability on 'CareProfessional'
        db.create_table('careprofessional_careprofessional_availability', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('careprofessional', models.ForeignKey(orm['careprofessional.careprofessional'], null=False)),
            ('availability', models.ForeignKey(orm['careprofessional.availability'], null=False))
        ))
        db.create_unique('careprofessional_careprofessional_availability', ['careprofessional_id', 'availability_id'])


    def backwards(self, orm):
        # Deleting model 'InstitutionType'
        db.delete_table('careprofessional_institutiontype')

        # Deleting model 'PostGraduate'
        db.delete_table('careprofessional_postgraduate')

        # Deleting model 'AcademicResume'
        db.delete_table('careprofessional_academicresume')

        # Deleting model 'Profession'
        db.delete_table('careprofessional_profession')

        # Deleting model 'ProfessionalProfile'
        db.delete_table('careprofessional_professionalprofile')

        # Removing M2M table for field agreement on 'ProfessionalProfile'
        db.delete_table('careprofessional_professionalprofile_agreement')

        # Removing M2M table for field workplace on 'ProfessionalProfile'
        db.delete_table('careprofessional_professionalprofile_workplace')

        # Deleting model 'LicenceBoard'
        db.delete_table('careprofessional_licenceboard')

        # Deleting model 'ProfessionalIdentification'
        db.delete_table('careprofessional_professionalidentification')

        # Deleting model 'StudentProfile'
        db.delete_table('careprofessional_studentprofile')

        # Deleting model 'Availability'
        db.delete_table('careprofessional_availability')

        # Deleting model 'CareProfessional'
        db.delete_table('careprofessional_careprofessional')

        # Removing M2M table for field availability on 'CareProfessional'
        db.delete_table('careprofessional_careprofessional_availability')


    models = {
        'address.address': {
            'Meta': {'object_name': 'Address'},
            'addressLine1': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'addressLine2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'addressNumber': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'addressPrefix': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'addressType': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['address.AddressType']"}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['address.City']", 'null': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'foreignCity': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'foreignCountry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['address.Country']", 'null': 'True'}),
            'foreignState': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'id': ('gestorpsi.util.uuid_field.UuidField', [], {'max_length': '36', 'primary_key': 'True'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'zipCode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        'address.addresstype': {
            'Meta': {'ordering': "['weight']", 'object_name': 'AddressType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'address.city': {
            'Meta': {'ordering': "['name']", 'object_name': 'City'},
            'ibge_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['address.State']"})
        },
        'address.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nationality': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'address.state': {
            'Meta': {'ordering': "['name']", 'object_name': 'State'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['address.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'shortName': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'careprofessional.academicresume': {
            'Meta': {'object_name': 'AcademicResume'},
            'area': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'course': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'finalDateGraduation': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'finalDatePostGraduate': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('gestorpsi.util.uuid_field.UuidField', [], {'max_length': '36', 'primary_key': 'True'}),
            'initialDateGraduation': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'initialDatePostGraduate': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'institutionType': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['careprofessional.InstitutionType']", 'unique': 'True', 'null': 'True'}),
            'lattesResume': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'postGraduate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['careprofessional.PostGraduate']", 'null': 'True'}),
            'teachingInstitute': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        'careprofessional.availability': {
            'Meta': {'object_name': 'Availability'},
            'day': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hour': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'careprofessional.careprofessional': {
            'Meta': {'ordering': "['person']", 'object_name': 'CareProfessional'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'availability': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['careprofessional.Availability']", 'symmetrical': 'False'}),
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'id': ('gestorpsi.util.uuid_field.UuidField', [], {'max_length': '36', 'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['person.Person']", 'unique': 'True'}),
            'professionalIdentification': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['careprofessional.ProfessionalIdentification']", 'unique': 'True', 'null': 'True'}),
            'professionalProfile': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['careprofessional.ProfessionalProfile']", 'unique': 'True', 'null': 'True'})
        },
        'careprofessional.institutiontype': {
            'Meta': {'ordering': "['description']", 'object_name': 'InstitutionType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'careprofessional.licenceboard': {
            'Meta': {'object_name': 'LicenceBoard'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'})
        },
        'careprofessional.postgraduate': {
            'Meta': {'ordering': "['description']", 'object_name': 'PostGraduate'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'careprofessional.profession': {
            'Meta': {'ordering': "['type']", 'object_name': 'Profession'},
            'academic_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'symbol_desc': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'})
        },
        'careprofessional.professionalidentification': {
            'Meta': {'object_name': 'ProfessionalIdentification'},
            'id': ('gestorpsi.util.uuid_field.UuidField', [], {'max_length': '36', 'primary_key': 'True'}),
            'profession': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['careprofessional.Profession']", 'null': 'True'}),
            'registerNumber': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'})
        },
        'careprofessional.professionalprofile': {
            'Meta': {'object_name': 'ProfessionalProfile'},
            'academicResume': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['careprofessional.AcademicResume']", 'unique': 'True', 'null': 'True'}),
            'agreement': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['organization.Agreement']", 'null': 'True', 'symmetrical': 'False'}),
            'availableTime': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'id': ('gestorpsi.util.uuid_field.UuidField', [], {'max_length': '36', 'primary_key': 'True'}),
            'initialProfessionalActivities': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'profession': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['careprofessional.Profession']", 'unique': 'True', 'null': 'True'}),
            'services': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'workplace': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['place.Place']", 'null': 'True', 'symmetrical': 'False'})
        },
        'careprofessional.studentprofile': {
            'Meta': {'object_name': 'StudentProfile'},
            'class_duration': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lecture_class': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['careprofessional.Profession']", 'null': 'True', 'blank': 'True'}),
            'period': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'professional': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['careprofessional.CareProfessional']", 'unique': 'True'}),
            'register_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'document.document': {
            'Meta': {'object_name': 'Document'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'document': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('gestorpsi.util.uuid_field.UuidField', [], {'max_length': '36', 'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['document.Issuer']", 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['address.State']", 'null': 'True', 'blank': 'True'}),
            'typeDocument': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['document.TypeDocument']"})
        },
        'document.issuer': {
            'Meta': {'ordering': "['description']", 'object_name': 'Issuer'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'document.typedocument': {
            'Meta': {'ordering': "['description']", 'object_name': 'TypeDocument'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'gcm.paymenttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'PaymentType'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'detail': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'show_to_client': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'time': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'gcm.plan': {
            'Meta': {'ordering': "['weight']", 'object_name': 'Plan'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pagseguro_code': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'staff_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'visible_client': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        'internet.email': {
            'Meta': {'object_name': 'Email'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'email_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['internet.EmailType']"}),
            'id': ('gestorpsi.util.uuid_field.UuidField', [], {'max_length': '36', 'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '36'})
        },
        'internet.emailtype': {
            'Meta': {'ordering': "['description']", 'object_name': 'EmailType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'internet.imnetwork': {
            'Meta': {'ordering': "['description']", 'object_name': 'IMNetwork'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'internet.instantmessenger': {
            'Meta': {'object_name': 'InstantMessenger'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('gestorpsi.util.uuid_field.UuidField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['internet.IMNetwork']", 'blank': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '36'})
        },
        'internet.site': {
            'Meta': {'object_name': 'Site'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('gestorpsi.util.uuid_field.UuidField', [], {'max_length': '36', 'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'site': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'organization.activitie': {
            'Meta': {'ordering': "['description']", 'object_name': 'Activitie'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'organization.administrationenvironment': {
            'Meta': {'ordering': "['description']", 'object_name': 'AdministrationEnvironment'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'organization.agreement': {
            'Meta': {'ordering': "['description']", 'object_name': 'Agreement'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'organization.dependence': {
            'Meta': {'ordering': "['description']", 'object_name': 'Dependence'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'organization.management': {
            'Meta': {'ordering': "['description']", 'object_name': 'Management'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'organization.organization': {
            'Meta': {'ordering': "['name']", 'object_name': 'Organization'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.Activitie']", 'null': 'True', 'blank': 'True'}),
            'city_inscription': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'cnes': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'contact_owner': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'contact_owner'", 'null': 'True', 'blank': 'True', 'to': "orm['person.Person']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'default_payment_day': ('django.db.models.fields.PositiveIntegerField', [], {'default': '10'}),
            'dependence': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.Dependence']", 'null': 'True', 'blank': 'True'}),
            'employee_number': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'environment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.AdministrationEnvironment']", 'null': 'True', 'blank': 'True'}),
            'id': ('gestorpsi.util.uuid_field.UuidField', [], {'max_length': '36', 'primary_key': 'True'}),
            'last_id_record': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'management': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.Management']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'organization_related'", 'null': 'True', 'to': "orm['organization.Organization']"}),
            'payment_detail': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'payment_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gcm.PaymentType']", 'null': 'True', 'blank': 'True'}),
            'person_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.PersonType']", 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'prefered_plan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gcm.Plan']", 'null': 'True', 'blank': 'True'}),
            'provided_type': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['organization.ProvidedType']", 'null': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'register_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.Source']", 'null': 'True', 'blank': 'True'}),
            'state_inscription': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'suspension': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'suspension_reason': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'trade_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'unit_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.UnitType']", 'null': 'True', 'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'organization.persontype': {
            'Meta': {'ordering': "['description']", 'object_name': 'PersonType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'organization.providedtype': {
            'Meta': {'ordering': "['description']", 'object_name': 'ProvidedType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'organization.source': {
            'Meta': {'ordering': "['description']", 'object_name': 'Source'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'organization.unittype': {
            'Meta': {'ordering': "['description']", 'object_name': 'UnitType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'person.maritalstatus': {
            'Meta': {'ordering': "['description']", 'object_name': 'MaritalStatus'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'person.person': {
            'Meta': {'ordering': "['name']", 'object_name': 'Person'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'birthDate': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'birthDateSupposed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'birthForeignCity': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'birthForeignCountry': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True'}),
            'birthForeignState': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'birthPlace': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['address.City']", 'null': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('gestorpsi.util.uuid_field.UuidField', [], {'max_length': '36', 'primary_key': 'True'}),
            'maritalStatus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['person.MaritalStatus']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['organization.Organization']", 'symmetrical': 'False'}),
            'photo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['auth.User']"})
        },
        'phone.phone': {
            'Meta': {'object_name': 'Phone'},
            'area': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'ext': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'id': ('gestorpsi.util.uuid_field.UuidField', [], {'max_length': '36', 'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'phoneNumber': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'phoneType': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phone.PhoneType']"})
        },
        'phone.phonetype': {
            'Meta': {'ordering': "['description']", 'object_name': 'PhoneType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'place.place': {
            'Meta': {'ordering': "['label']", 'object_name': 'Place'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'hour_end': ('django.db.models.fields.CharField', [], {'default': "'19,00'", 'max_length': '10'}),
            'hour_start': ('django.db.models.fields.CharField', [], {'default': "'07,00'", 'max_length': '10'}),
            'id': ('gestorpsi.util.uuid_field.UuidField', [], {'max_length': '36', 'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.Organization']", 'null': 'True', 'blank': 'True'}),
            'place_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['place.PlaceType']"})
        },
        'place.placetype': {
            'Meta': {'ordering': "['description']", 'object_name': 'PlaceType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['careprofessional']