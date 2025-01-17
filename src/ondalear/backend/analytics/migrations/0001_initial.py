# Generated by Django 2.2.3 on 2019-09-26 00:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('docmgmt', '0010_non_unique_upload'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisResults',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('version', models.IntegerField(default=0)),
                ('is_enabled', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('input', jsonfield.fields.JSONField()),
                ('output', jsonfield.fields.JSONField()),
                ('name', models.CharField(blank=True, max_length=256, null=True)),
                ('description', models.TextField(blank=True, max_length=2048, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docmgmt.Client')),
                ('creation_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='analytics_analysisresults_related_creation_user', to=settings.AUTH_USER_MODEL)),
                ('documents', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='docmgmt.DocumentAssociation')),
                ('effective_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='analytics_analysisresults_related_effective_user', to=settings.AUTH_USER_MODEL)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='analytics_analysisresults_related_site', to='sites.Site')),
                ('update_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='analytics_analysisresults_related_update_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Analysis results',
                'verbose_name_plural': 'Analysis results',
                'db_table': 'ondalear_analytics_analysis_results',
                'get_latest_by': 'update_time',
                'abstract': False,
            },
        ),
    ]
