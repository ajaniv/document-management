# Generated by Django 2.2.3 on 2019-08-12 22:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docmgmt', '0007_remove_document_has_logged_in'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientuser',
            name='login_count',
        ),
    ]