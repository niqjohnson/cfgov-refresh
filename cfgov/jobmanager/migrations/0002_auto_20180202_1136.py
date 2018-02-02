# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):
    replaces = [
        ('jobmanager', '0002_auto_20160809_1619'),
        ('jobmanager', '0003_auto_20160814_2044'),
        ('jobmanager', '0004_auto_20160815_1008'),
        ('jobmanager', '0005_auto_20160815_1457'),
        ('jobmanager', '0006_auto_20160815_1705'),
        ('jobmanager', '0007_create_careers_pages'),
        ('jobmanager', '0008_migrate_job_pages'),
        ('jobmanager', '0009_django_cleanup'),
        ('jobmanager', '0010_cleanup_unused_fields'),
        ('jobmanager', '0011_delete_fellowshipupdatelist'),
        ('jobmanager', '0012_jobs_have_one_region'),
    ]

    dependencies = [
        ('jobmanager', '0001_initial'),
        ('v1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobListingPage',
            fields=[
                ('cfgovpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.CFGOVPage')),
                ('description', wagtail.wagtailcore.fields.RichTextField(verbose_name=b'Description')),
                ('open_date', models.DateField(verbose_name=b'Open date')),
                ('close_date', models.DateField(verbose_name=b'Close date')),
                ('salary_min', models.DecimalField(verbose_name=b'Minimum salary', max_digits=11, decimal_places=2)),
                ('salary_max', models.DecimalField(verbose_name=b'Maximum salary', max_digits=11, decimal_places=2)),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='jobmanager.JobCategory', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.cfgovpage',),
        ),
        migrations.CreateModel(
            name='JobRegion',
            fields=[
                ('abbreviation', models.CharField(max_length=2, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('abbreviation',),
            },
        ),
        migrations.CreateModel(
            name='USAJobsApplicationLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('announcement_number', models.CharField(max_length=128)),
                ('url', models.URLField(max_length=255)),
                ('applicant_type', models.ForeignKey(related_name='usajobs_application_links', to='jobmanager.ApplicantType')),
                ('job_listing', modelcluster.fields.ParentalKey(related_name='usajobs_application_links', to='jobmanager.JobListingPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='joblistingpage',
            name='region',
            field=models.ForeignKey(related_name='job_listings', on_delete=django.db.models.deletion.PROTECT, to='jobmanager.JobRegion'),
        ),
        migrations.AddField(
            model_name='gradepanel',
            name='grade',
            field=models.ForeignKey(related_name='grade_panels', to='jobmanager.Grade'),
        ),
        migrations.AddField(
            model_name='gradepanel',
            name='job_listing',
            field=modelcluster.fields.ParentalKey(related_name='grades', to='jobmanager.JobListingPage'),
        ),
        migrations.AddField(
            model_name='emailapplicationlink',
            name='job_listing',
            field=modelcluster.fields.ParentalKey(related_name='email_application_links', to='jobmanager.JobListingPage'),
        ),
    ]
